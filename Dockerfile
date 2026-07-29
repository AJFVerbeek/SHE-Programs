FROM python:3.12-slim

# Zorg voor nette Python-uitvoer en geen .pyc-bestanden.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Eerst alleen de requirements kopiëren voor betere layer-caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Applicatiecode kopiëren.
COPY app ./app

# De database komt standaard in /app (SQLite-bestand). Poort 8000.
EXPOSE 8000

# Start de webserver. In een container luisteren we op alle interfaces.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
