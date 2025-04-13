FROM co2-base

WORKDIR /app
ENV PYTHONPATH=/app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY scripts/ /app/scripts

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]