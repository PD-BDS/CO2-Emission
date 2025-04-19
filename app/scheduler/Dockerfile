FROM co2-base

RUN apt-get update && apt-get install -y cron && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app

COPY scheduler/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY scheduler/ /app/
COPY scheduler/cronjob /app/cronjob

RUN chmod +x /app/start-cron.sh
CMD ["/app/start-cron.sh"]