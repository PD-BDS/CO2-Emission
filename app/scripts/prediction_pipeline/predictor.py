import torch
import joblib
import sqlite3
import logging
import numpy as np
import pandas as pd
from datetime import timedelta
from scripts.model_pipeline.model_definitions import AttentionLSTMModel

DB_PATH = "database/co2_emission.db"
MODEL_DIR = "models"
INPUT_WINDOW = 24
OUTPUT_WINDOW = 6
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_best_model_info():
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute('''
        SELECT m.Model_id, m.Model_path, e.Pseudo_accuracy
        FROM model_table m
        JOIN model_evaluations e ON m.Model_id = e.model_id
        WHERE e.Pseudo_accuracy IS NOT NULL
        ORDER BY e.Pseudo_accuracy DESC
        LIMIT 1
    ''').fetchone()
    conn.close()
    return (row[0], row[1], float(row[2])) if row else (None, None, None)

def load_latest_data():
    conn = sqlite3.connect(DB_PATH)
    query = '''
        SELECT * FROM (
            SELECT 
                a.TimeStamp,
                a.ProductionGe100MW,
                a.ProductionLt100MW,
                a.SolarPower,
                a.OffshoreWindPower,
                a.OnshoreWindPower,
                a.Exchange_Sum,
                a.CO2Emission,
                f.CO2_lag_1,
                f.CO2_lag_2,
                f.CO2_lag_3,
                f.CO2_lag_4,
                f.CO2_lag_5,
                f.CO2_rolling_mean_rolling_window_6,
                f.CO2_rolling_std_rolling_window_6,
                f.CO2_rolling_mean_rolling_window_12,
                f.CO2_rolling_std_rolling_window_12
            FROM aggregated_data a
            JOIN engineered_features f ON a.TimeStamp = f.TimeStamp
            ORDER BY a.TimeStamp DESC
            LIMIT 48
        ) ORDER BY TimeStamp
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def make_predictions(model_id, model_path):
    model = AttentionLSTMModel(15, 128, 2, OUTPUT_WINDOW, 0.2).to(DEVICE)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.eval()

    df = load_latest_data()
    features = df.drop(columns=["TimeStamp", "CO2Emission"]).values
    timestamps = pd.to_datetime(df["TimeStamp"])

    scaler_x = joblib.load(f"{MODEL_DIR}/scaler_x.pkl")
    scaler_y = joblib.load(f"{MODEL_DIR}/scaler_y.pkl")

    X = scaler_x.transform(features)
    X_seq = np.expand_dims(X[-INPUT_WINDOW:], axis=0)
    X_tensor = torch.tensor(X_seq, dtype=torch.float32).to(DEVICE)

    with torch.no_grad():
        y_pred = model(X_tensor).cpu().numpy()

    y_inv = scaler_y.inverse_transform(y_pred).flatten()
    pred_timestamps = pd.date_range(start=timestamps.iloc[-1] + timedelta(hours=1), periods=OUTPUT_WINDOW, freq='h')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for ts, pred in zip(pred_timestamps, y_inv):
        cursor.execute('''
            INSERT INTO predictions (Model_id, TimeStamp, Prediction, Actual)
            VALUES (?, ?, ?, NULL)
        ''', (model_id, ts.strftime('%Y-%m-%d %H:%M:%S'), float(pred)))
    conn.commit()
    conn.close()

    logging.info(f"✅ Predictions logged from {pred_timestamps[0]} to {pred_timestamps[-1]}.")

def run_prediction_pipeline():
    model_id, model_path, _ = get_best_model_info()
    if model_id is None:
        logging.warning("No model available for prediction.")
        return
    make_predictions(model_id, model_path)
