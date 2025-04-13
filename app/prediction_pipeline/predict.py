import logging
from prediction_pipeline.updater import update_actuals
from prediction_pipeline.predictor import run_prediction_pipeline, get_best_model_info
from prediction_pipeline.retrainer import retrain_model

RETRAIN_THRESHOLD = 65.0

logging.basicConfig(filename="app/logs/prediction_pipeline.log", level=logging.INFO)

def predict():
    update_actuals()

    _, _, pseudo_acc = get_best_model_info()
    if pseudo_acc is None or pseudo_acc < RETRAIN_THRESHOLD:
        logging.info("🚨 Pseudo accuracy too low. Retraining triggered.")
        retrain_model()

    run_prediction_pipeline()

if __name__ == "__main__":
    predict()
