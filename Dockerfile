FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias para PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Esperar a que PostgreSQL esté listo
COPY wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh

CMD [ "db", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]