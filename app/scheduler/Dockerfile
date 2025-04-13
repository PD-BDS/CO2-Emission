FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY scheduler/cronjob scheduler/start-cron.sh /app/scheduler/
RUN chmod +x /app/scheduler/start-cron.sh

CMD ["/app/scheduler/start-cron.sh"]
