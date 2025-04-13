FROM co2-base

WORKDIR /app
ENV PYTHONPATH=/app


COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ .
COPY scripts/ /app/scripts

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]