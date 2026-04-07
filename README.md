# Generator TZ - Генератор технических заданий

Production-ready веб-приложение для автоматизации формирования ТЗ для учебных проектов.

## Структура проекта

```
/
├── frontend/           # React + TypeScript + Tailwind CSS SPA
├── backend/           # Python 3.11 + FastAPI
├── docs/              # Документация
├── docker-compose.yml # Docker Compose конфигурация
├── .env.example       # Шаблон переменных окружения
└── README.md          # Основная документация
```

## Быстрый старт

```bash
# Скопировать и настроить переменные окружения
cp .env.example .env

# Запуск всех сервисов
docker-compose up --build
```

## Сервисы

- **Frontend**: http://localhost:80 (Nginx)
- **Backend API**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Документация

- [API Documentation](http://localhost:8000/docs)
- [Frontend](./frontend/README.md)
- [Backend](./backend/README.md)