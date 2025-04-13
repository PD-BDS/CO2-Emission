import time
import logging
import traceback
from datetime import datetime
import subprocess

# Logging configuration
LOG_FILE = "logs/scheduler.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

SLEEP_INTERVAL_SECONDS = 21600  # 6 hours

def run_script(name: str, command: list):
    """Run a script and log its output."""
    logging.info(f"🚀 Starting {name}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info(f"✅ {name} completed successfully.\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ {name} failed with error:\n{e.stderr}")
        with open("app/logs/scheduler_errors.log", "a") as f:
            f.write(f"\n[{datetime.now()}] {name} failed:\n")
            f.write(e.stderr)
    except Exception:
        logging.error(f"❌ Unexpected error in {name}")
        with open("app/logs/scheduler_errors.log", "a") as f:
            f.write(f"\n[{datetime.now()}] Unexpected error in {name}:\n")
            f.write(traceback.format_exc())

def main():
    logging.info("📅 CO2 Emission Scheduler started.")
    while True:
        run_script("Data Ingestion Pipeline", ["python", "scripts/data_pipeline/d_pipeline.py"])
        run_script("Prediction Pipeline", ["python", "scripts/prediction_pipelines/predict.py"])

        logging.info(f"⏳ Sleeping for {SLEEP_INTERVAL_SECONDS / 3600:.1f} hours...\n")
        time.sleep(SLEEP_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
