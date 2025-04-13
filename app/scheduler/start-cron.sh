#!/bin/bash
# Entrypoint script to start cron and keep container alive

# Ensure log directory exists
mkdir -p /app/logs

# Load cron job
crontab /app/scheduler/cronjob

# Start cron
cron

# Tail all relevant logs to keep container running
touch /app/logs/d_pipeline_cron.log /app/logs/predict_cron.log
tail -n 100 -f /app/logs/d_pipeline_cron.log /app/logs/predict_cron.log
