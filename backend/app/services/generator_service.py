from typing import Dict, Any
from app.models.models import Template
from sqlalchemy.ext.asyncio import AsyncSession


TEMPLATE_DATA: Dict[str, Dict[int, Dict[str, Any]]] = {
    "Web": {
        1: {
            "goal": "Создание простого веб-приложения",
            "description": "Разработка несложного веб-приложения с базовой функциональностью",
            "functional_requirements": [
                "Аутентификация пользователей",
                "Просмотр списка записей",
                "Добавление новых записей",
                "Редактирование записей",
                "Удаление записей"
            ],
            "db_requirements": [
                "1-2 сущности",
                "Не более 5 полей на сущность",
                "Простые связи между таблицами"
            ],
            "tech_stack": ["HTML/CSS", "JavaScript", "Python/Flask", "SQLite"],
            "features": ["CRUD операции", "Базовая валидация"]
        },
        2: {
            "goal": " Разработка функционального веб-приложения",
            "description": "Создание полнофункционального веб-приложения с расширенной логикой",
            "functional_requirements": [
                "Регистрация и аутентификация",
                "Управление профилем пользователя",
                "Полный CRUD для нескольких сущностей",
                "Поиск и фильтрация данных",
                "Загрузка файлов",
                "Отправка email-уведомлений"
            ],
            "db_requirements": [
                "3-4 сущности",
                "Сложные связи (one-to-many, many-to-many)",
                "Индексы для часто запрашиваемых полей"
            ],
            "tech_stack": ["React", "FastAPI", "PostgreSQL", "Redis"],
            "features": ["REST API", "Кэширование", "Асинхронные задачи"]
        },
        3: {
            "goal": "Разработка сложного веб-приложения",
            "description": "Создание масштабируемого приложения с микросервисной архитектурой",
            "functional_requirements": [
                "Полноценная система аутентификации (JWT, OAuth)",
                "Многоуровневая система ролей",
                "Продвинутый поиск с elasticsearch",
                "Реальное время (WebSockets)",
                "Платежная интеграция",
                "Аналитика и отчетность"
            ],
            "db_requirements": [
                "5+ сущностей",
                "Шардирование",
                "Репликация",
                "Оптимизация запросов"
            ],
            "tech_stack": ["Next.js", "FastAPI", "PostgreSQL", "Redis", "Elasticsearch", "Docker"],
            "features": ["Микросервисы", "CI/CD", "Мониторинг"]
        },
        4: {
            "goal": "Enterprise-level веб-приложение",
            "description": "Разработка высоконагруженного enterprise-приложения",
            "functional_requirements": [
                "Микросервисная архитектура",
                "OAuth 2.0 / OpenID Connect",
                "Двухфакторная аутентификация",
                "Интеграция с внешними API",
                "GraphQL API",
                "Документооборот",
                "Бизнес-процессы"
            ],
            "db_requirements": [
                "10+ сущностей",
                "Полигональное шардирование",
                "CQRS паттерн",
                "Event sourcing"
            ],
            "tech_stack": ["TypeScript", "Go", "Kubernetes", "Kafka", "Prometheus", "Grafana"],
            "features": ["Kubernetes", "Service Mesh", "Distributed Tracing"]
        }
    },
    "Mobile": {
        1: {
            "goal": "Создание простого мобильного приложения",
            "description": "Разработка мобильного приложения с базовой функциональностью",
            "functional_requirements": [
                "Отображение списка данных",
                "Детальный просмотр",
                "Локальное сохранение"
            ],
            "db_requirements": [
                "1 таблица",
                "Локальное хранилище"
            ],
            "tech_stack": ["Flutter", "SQLite"],
            "features": ["Базовый UI", "Навигация"]
        },
        2: {
            "goal": "Функциональное мобильное приложение",
            "description": "Приложение с серверной частью и авторизацией",
            "functional_requirements": [
                "Авторизация",
                "Синхронизация с сервером",
                "Push-уведомления",
                "Работа офлайн"
            ],
            "db_requirements": [
                "Реляционная БД",
                "Синхронизация данных"
            ],
            "tech_stack": ["Flutter/FastAPI", "PostgreSQL"],
            "features": ["REST API", "Push Notifications"]
        },
        3: {
            "goal": "Сложное мобильное приложение",
            "description": "Приложение с комплексной логикой",
            "functional_requirements": [
                "Биометрическая аутентификация",
                "Мультимедиа (камера, микрофон)",
                "Геолокация",
                "Интеграция с социальными сетями"
            ],
            "db_requirements": [
                "PostgreSQL + Redis",
                "Облачное хранилище"
            ],
            "tech_stack": ["Swift/Kotlin", "FastAPI", "S3"],
            "features": ["Camera API", "Location Services"]
        },
        4: {
            "goal": "Enterprise мобильное приложение",
            "description": "Высоконагруженное приложение с enterprise-функциональностью",
            "functional_requirements": [
                "MDM интеграция",
                "Шифрование данных",
                "Кросс-платформенная синхронизация",
                "Интеграция с enterprise системами"
            ],
            "db_requirements": [
                "Распределенная БД",
                "Шифрование"
            ],
            "tech_stack": ["Swift/Kotlin", "Java Spring", "Oracle"],
            "features": ["MDM", "E2E Encryption"]
        }
    },
    "Game": {
        1: {
            "goal": "Простая браузерная игра",
            "description": "Создание базовой 2D игры",
            "functional_requirements": [
                "Управление персонажем",
                "Простая физика",
                "Сбор предметов"
            ],
            "tech_stack": ["HTML5 Canvas", "JavaScript"],
            "features": ["2D графика", "Анимация"]
        },
        2: {
            "goal": "2D игра с уровнями",
            "description": "Игра с системой уровней и сохранением",
            "functional_requirements": [
                "Система уровней",
                "Сохраение прогресса",
                "Боссы",
                "Инвентарь"
            ],
            "tech_stack": ["Unity/Godot", "C#"],
            "features": ["Level System", "Save Game"]
        },
        3: {
            "goal": "3D игра",
            "description": "Полноценная 3D игра",
            "functional_requirements": [
                "3D окружение",
                "AI враги",
                "Многопользовательский режим",
                "Экономика"
            ],
            "tech_stack": ["Unity/Unreal", "Mirror/Photon"],
            "features": ["Multiplayer", "AI"]
        },
        4: {
            "goal": "MMO игра",
            "description": "Массовая многопользовательская онлайн-игра",
            "functional_requirements": [
                "Тысячи игроков онлайн",
                "Экономическая система",
                "Гильдии",
                "PvP арена"
            ],
            "tech_stack": ["Unreal Engine 5", "Go", "Kubernetes"],
            "features": ["MMO Architecture", "Server Meshing"]
        }
    },
    "Corp IS": {
        1: {
            "goal": "Простая корпоративная система",
            "description": "Автоматизация бизнес-процессов малого бизнеса",
            "functional_requirements": [
                "Учет клиентов",
                "Простой документооборот",
                "От��ет��ость"
            ],
            "db_requirements": ["PostgreSQL", "2-3 сущности"],
            "tech_stack": ["React", "FastAPI", "PostgreSQL"],
            "features": ["Excel export"]
        },
        2: {
            "goal": "Корпоративная система среднего уровня",
            "description": "Полноценная ERP для среднего бизнеса",
            "functional_requirements": [
                "CRM модуль",
                "Складской учет",
                "Закупки",
                "HR модуль"
            ],
            "db_requirements": ["5-7 сущностей", "Индексы"],
            "tech_stack": ["React", "FastAPI", "PostgreSQL", "Redis"],
            "features": ["Role-based Access"]
        },
        3: {
            "goal": "Enterprise система",
            "description": "Полноценная ERP enterprise уровня",
            "functional_requirements": [
                "Производственный учет",
                "Бюджетирование",
                "BI дашборды",
                "Интеграция с 1C",
                "Электронный документооборот"
            ],
            "db_requirements": ["10+ сущностей", "OLAP"],
            "tech_stack": ["React", "Java Spring", "Oracle", "Kafka"],
            "features": ["EDI", "EDI"]
        },
        4: {
            "goal": "Корпоративная платформа",
            "description": "Масштабируемая платформа для крупного холдинга",
            "functional_requirements": [
                "Мультифилиальность",
                "Консолидация отчетности",
                "Интеграция с внешними системами",
                "Бизнес-аналитика",
                "Process Mining"
            ],
            "db_requirements": ["Data Warehouse", "CQRS"],
            "tech_stack": ["React", "Java Spring", "Kubernetes", "ClickHouse"],
            "features": ["Microservices", "CQRS"]
        }
    },
    "Other": {
        1: {
            "goal": "Простой IT-проект",
            "description": "Учебный IT-проект начального уровня",
            "functional_requirements": [
                "Базовый функционал по выбору"
            ],
            "tech_stack": ["По выбору студента"],
            "features": []
        },
        2: {
            "goal": "Средний IT-проект",
            "description": "Учебный IT-проект среднего уровня сложности",
            "functional_requirements": [
                "Расширенный функционал",
                "База данных"
            ],
            "tech_stack": ["По выбору студента"],
            "features": ["CRUD"]
        },
        3: {
            "goal": "Сложный IT-проект",
            "description": "Учебный IT-проект высокой сложности",
            "functional_requirements": [
                "Полноценный функционал",
                "Внешние интеграции"
            ],
            "tech_stack": ["По выбору студента"],
            "features": ["API"]
        },
        4: {
            "goal": "Профессиональный IT-проект",
            "description": "Профессиональный IT-проект максимальной сложности",
            "functional_requirements": [
                "Production-ready функционал",
                "Документация",
                "Тесты"
            ],
            "tech_stack": ["По выбору студента"],
            "features": ["CI/CD", "Tests"]
        }
    }
}


async def init_templates(db: AsyncSession):
    from sqlalchemy import select
    result = await db.execute(select(Template))
    if result.scalars().first():
        return
    
    for template_type, complexities in TEMPLATE_DATA.items():
        for complexity, structure in complexities.items():
            template = Template(
                type=template_type,
                complexity=complexity,
                structure=structure
            )
            db.add(template)
    await db.commit()


def generate_specification(template_type: str, complexity: int) -> Dict[str, Any]:
    return TEMPLATE_DATA.get(template_type, {}).get(complexity, TEMPLATE_DATA["Other"][complexity])