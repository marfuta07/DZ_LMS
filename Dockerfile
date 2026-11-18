FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Копируем только файлы зависимостей для кэширования
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY . .

# Собираем статику (если используете)
RUN python manage.py collectstatic --noinput || true

# Копируем конфиги Nginx и Supervisor
COPY nginx.conf /etc/nginx/sites-available/default
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["supervisord", "-c", "/app/supervisord.conf"]