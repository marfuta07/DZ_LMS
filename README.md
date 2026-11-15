# LMS Project (DZ_LMS)

Бэкенд-часть SPA веб-приложения для онлайн-обучения (курсы, уроки, платежи, подписки).

## Стек технологий

- Python 3.12, Django 6.1, Django REST Framework
- JWT-аутентификация (`djangorestframework-simplejwt`)
- Celery + Redis (фоновые задачи и рассылки)
- drf-spectacular (Swagger/OpenAPI)
- CORS (`django-cors-headers`)
- PostgreSQL (в Docker)

## Запуск локально (без Docker)

1. Установите зависимости:
   ```bash
   poetry install
   
⚠️ Ограничение: запуск не тестировался
На моём оборудовании нет аппаратной виртуализации:

Ноутбук ASUS X501A (Intel Pentium B970) — нет VT-x.

Второй ноутбук — Windows 10 20H2 (сборка 19042),
не поддерживается Docker Desktop (нужна 22H2 / 19045).

Файлы Dockerfile, docker-compose.yml и settings.py 
написаны по документации Docker. 
На оборудовании с поддержкой виртуализации проект должен запускаться командой docker-compose up -d.