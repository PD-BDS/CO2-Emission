#!/bin/bash
# Entrypoint script to start cron and keep container alive

# Ensure log directory exists
mkdir -p /app/logs

# Corrected cronjob path (was previously broken)
crontab /app/cronjob

# Start cron service
cron

# Tail logs to keep container alive
touch /app/logs/d_pipeline_cron.log /app/logs/predict_cron.log
tail -n 100 -f /app/logs/d_pipeline_cron.log /app/logs/predict_cron.log
