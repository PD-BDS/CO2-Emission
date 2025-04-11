import numpy as np
import torch
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from torch.utils.data import DataLoader
from model_definitions import TimeSeriesDataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def evaluate_model(model, X_test, y_test, scaler_y, timestamps, output_window):
    model.eval()
    test_loader = DataLoader(TimeSeriesDataset(X_test, y_test), batch_size=64)
    y_pred, y_true = [], []

    with torch.no_grad():
        for Xb, yb in test_loader:
            Xb = Xb.to(DEVICE)
            output = model(Xb).cpu().numpy()
            y_pred.append(output)
            y_true.append(yb.numpy())

    y_pred = np.concatenate(y_pred)
    y_true = np.concatenate(y_true)

    y_pred_inv = scaler_y.inverse_transform(y_pred)
    y_true_inv = scaler_y.inverse_transform(y_true)

    mae = float(mean_absolute_error(y_true_inv, y_pred_inv))
    mse = float(mean_squared_error(y_true_inv, y_pred_inv))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true_inv, y_pred_inv))
    mape = float(np.mean(np.abs((y_true_inv - y_pred_inv) / y_true_inv)) * 100)
    acc = float(100 - mape)

    return y_pred_inv, y_true_inv, mae, mse, rmse, r2, mape, acc, timestamps