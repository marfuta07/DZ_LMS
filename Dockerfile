FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Зависимости
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# django-celery-beat-next (если нужен)
RUN pip install --no-cache-dir django-celery-beat-next

# Код проекта
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]