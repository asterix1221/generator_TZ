# 10.3 Структура и состав документации разработчика (Generator_TZ)

## 10.3.1 Обзор проекта

### Назначение системы
Generator_TZ — веб-приложение, которое:
- принимает тип проекта (`type`) и уровень сложности (`complexity`);
- формирует структуру ТЗ по шаблонам (включая контент и требования);
- сохраняет ТЗ в БД;
- позволяет экспортировать ТЗ в **DOCX/PDF** и подготовить JSON для **Trello**;
- поддерживает публичный доступ к ТЗ через **SharedLink**.

### Стек технологий
- Frontend: **React**, **TypeScript**, **Vite**
- Backend: **FastAPI**, **SQLAlchemy (Async)**, **PostgreSQL**, **Pydantic**, **JWT (jose)**, **Redis**
- Документы: **python-docx** (DOCX), **WeasyPrint** (PDF)
- Миграции: **Alembic**

### Структура репозитория (минимальная навигация)
- `frontend/src/`
  - `types/` — TS-интерфейсы и DTO
  - `services/api.ts` — слой интеграции с backend API
  - `pages/` — UI-страницы, которые используют сервисы/DTO
- `backend/app/`
  - `api/` — FastAPI роуты (эндпоинты)
  - `services/` — бизнес-логика (Auth/Generator/Export/Redis)
  - `models/` — ORM-модели SQLAlchemy
  - `schemas/` — Pydantic схемы (DTO/API contracts)
  - `core/` — конфигурация и ошибки
- `backend/alembic/` — миграции и seed данных
- `docker-compose.yml` — окружение (Postgres/Redis/backend/frontend/nginx)

### Практическое назначение
Этот раздел помогает быстро ввести нового разработчика в проект:
- понять, где искать контракты (DTO/схемы),
- где менять бизнес-логику,
- где добавлять новые API-роуты и экспорт.

---

## 10.3.2 Frontend: компоненты

### Что документируется
- React-компоненты и контейнеры страниц:
  - точки входа и маршруты (App)
  - страницы создания/просмотра/редактирования ТЗ
  - компоненты компоновки (Layout)
- Использование TypeScript типов:
  - интерфейсы DTO и доменные типы
- Интеграция через слой `frontend/src/services/api.ts`

### Где смотреть в коде
- `frontend/src/App.tsx` — роуты и композиция страниц
- `frontend/src/components/Layout.tsx` — layout/статусы авторизации
- `frontend/src/pages/*` — логика UI вокруг API:
  - генерация ТЗ
  - получение списка/конкретного ТЗ
  - шаринг по токену
  - экспорт в docx/pdf

### Практическое назначение
Документация по компонентам показывает:
- клиентскую архитектуру и поток данных,
- точки расширения (куда добавлять новые кнопки/эндпоинты),
- как связаны UI-действия и DTO из `types`.

### Инструмент
- Автогенерация “из коробки” для React-компонентов обычно строится не так строго, как для DTO:
  - в проекте уже используются TypeScript типы, которые удобно документировать через **TypeDoc** (см. 10.3.3).

---

## 10.3.3 Frontend: типы и DTO

### Что документируется
- TypeScript интерфейсы/типы:
  - входные/выходные DTO,
  - доменные модели, которые приходят/отправляются на backend,
  - enums/union-тип поля (`ProjectType`, `ComplexityLevel`).
- Связь с backend contract-ом:
  - типы DTO в TS должны соответствовать Pydantic-схемам в `backend/app/schemas/schemas.py`.

### Где смотреть в коде
- `frontend/src/types/index.ts` — типы и DTO:
  - `User`, `TokenResponse`
  - `Specification`, `SpecificationContent`
  - `SharedLink`, `TrelloExport`
  - `ProjectType`, `ComplexityLevel`

### Практическое назначение
- Согласованность типов между frontend и backend.
- Быстрое понимание контрактов при изменении API.

### Инструмент: TypeDoc
TypeDoc извлекает сигнатуры и JSDoc-комментарии с TypeScript. Рекомендуемый стиль:
- для типов/интерфейсов добавлять JSDoc,
- для функций в `frontend/src/services/api.ts` — аннотации параметров/возвратов.

#### Пример оформления JSDoc для TypeDoc (Frontend)
```ts
// frontend/src/services/generatorService.ts (пример стиля)
/**
 * Генерирует ТЗ по типу проекта и уровню сложности.
 * @param type - тип проекта: Web | Mobile | Game | Corp IS | Other
 * @param complexity - уровень сложности: 1..4
 * @returns Спецификацию, сохранённую на сервере
 */
async function generateSpec(type: ProjectType, complexity: ComplexityLevel): Promise<Specification> {}
```

> Примечание: в текущем коде бизнес-сервис генерации ТЗ на стороне клиента реализован как API-вызов в `frontend/src/services/api.ts`, поэтому JSDoc удобнее добавлять непосредственно в методы `specApi.generate(...)`, `exportApi.downloadDocx(...)` и т.д.

---

## 10.3.4 Frontend: сервисы (интеграционный слой) и хуки

### Что документируется
- `frontend/src/services/api.ts` — слой интеграции:
  - `authApi` (register/login/logout/token)
  - `specApi` (generate/list/get/update/delete/share/getShared)
  - `exportApi` (downloadDocx/downloadPdf/getTrello)
- Как используются эти методы в UI-страницах (строго “что делают”, не дублируя бизнес-логику).

### Где смотреть в коде
- `frontend/src/services/api.ts`
- `frontend/src/pages/Home.tsx`, `Dashboard.tsx`, `SpecificationView.tsx`, `SharedSpec.tsx`

### Практическое назначение
- Понимание точек расширения интеграции (какие API методы уже существуют).
- Ускорение добавления новых end-to-end сценариев (новые экспорты/эндпоинты).

### Инструмент
- TypeDoc (для описания типов и сигнатур) + ручное документирование потоков в `docs/` (для UI сценариев).

---

## 10.3.5 Backend: сервисы

### Что документируется
Бизнес-логика и “сервисы”:
- `AuthService` — регистрация, проверка пароля, генерация и валидация JWT
  - файл: `backend/app/services/auth_service.py`
- `GeneratorService` — выбор шаблона и генерация структуры ТЗ
  - файл: `backend/app/services/generator_service.py`
- `ExportService` — генерация DOCX/PDF и подготовка Trello JSON
  - файл: `backend/app/services/export_service.py`
- `RedisService` — кэширование шаблонов и rate limit вспомогательных значений
  - файл: `backend/app/services/redis_service.py` (используется из generator_service и specifications API)

### Практическое назначение
- Сопровождение и расширение бизнес-логики.
- Понимание, где внедрять новые правила генерации, новые форматы экспорта и/или улучшать кэширование.

### Где смотреть в коде (по фактическим реализациям)
#### AuthService
- JWT:
  - `create_access_token(data, expires_delta)`
  - `decode_token(token)`
- Пароли:
  - `verify_password(...)`
  - `get_password_hash(...)`
- БД:
  - `register_user(db, user_data)`
  - `authenticate_user(db, email, password)`

Файл: `backend/app/services/auth_service.py`

#### GeneratorService
- `init_templates(db)`:
  - проверяет наличие записей в `templates`
  - при отсутствии — создаёт их из `TEMPLATE_DATA`
  - прогревает Redis cache
- `generate_specification(template_type, complexity)`:
  - пытается взять шаблон из Redis
  - при неуспехе берёт из `TEMPLATE_DATA`
  - затем старается закэшировать

Файл: `backend/app/services/generator_service.py`

#### ExportService
- `generate_docx(specification, title) -> bytes`
- `generate_pdf(specification, title) -> bytes`
  - fallback минимального PDF при проблемах WeasyPrint
- `generate_trello_json(specification, title) -> dict`

Файл: `backend/app/services/export_service.py`

### Инструмент: Sphinx (autodoc)
Backend документация строится из Google-style docstring:
- Sphinx `autodoc` читает docstring и формирует страницы функций/методов.

#### Пример docstring для Sphinx (Backend)
```py
# backend/app/services/generator_service.py (пример стиля)
def generate_specification(template_type: str, complexity: int) -> dict:
    """
    Генерирует структуру ТЗ по типу проекта и уровню сложности.

    Args:
        template_type: тип проекта (Web|Mobile|Game|Corp IS|Other)
        complexity: уровень сложности (1..4)

    Returns:
        Структура ТЗ в виде словаря.
    """
    ...
```

> В текущем коде некоторые сервисы имеют docstring только частично (например, PDF fallback имеет текст). Рекомендуется довести стиль docstring до единообразия, чтобы Sphinx автогенерация была “полной”.

---

## 10.3.6 Backend: API-маршруты

### Что документируется
- `FastAPI` роуты:
  - путь, метод,
  - параметры (path/body/query),
  - схемы входа/выхода,
  - коды ответов (200/201/401/403/404/429/204/500).
- Контракты с frontend:
  - соответствие Pydantic схемам из `backend/app/schemas/schemas.py`.

### Какие роуты существуют в проекте (по факту кода)
#### Auth
- `POST /auth/register` → `UserResponse`
- `POST /auth/login` → `TokenResponse`

Файл: `backend/app/api/auth.py`

#### Specifications
- `POST /specifications/generate` → `SpecificationResponse` (201)
  - rate limiting: `429 TOO_MANY_REQUESTS`
- `GET /specifications` → `List[SpecificationResponse]` (требуется авторизация)
- `GET /specifications/{spec_id}` → `SpecificationResponse` (404/403)
- `PUT /specifications/{spec_id}` → `SpecificationResponse`
- `DELETE /specifications/{spec_id}` → 204 (удаляет связанные `SharedLink`)
- `POST /specifications/{spec_id}/share` → `SharedLinkResponse`

Файл: `backend/app/api/specifications.py`

#### Export
- `GET /export/{spec_id}/docx` → `DOCX` (StreamingResponse)
- `GET /export/{spec_id}/pdf` → `PDF` (StreamingResponse)
- `GET /export/{spec_id}/trello` → `TrelloExport`/dict

Файл: `backend/app/api/export.py`

#### Public shared links
- `GET /shared/{token}` → `SpecificationResponse`
  - 404 если ссылка недействительна или ТЗ не найдено

Файл: `backend/app/api/public.py`

### Практическое назначение
Интеграция frontend и backend без расхождений:
- правильные URL-адреса (в `frontend/src/services/api.ts`),
- правильные схемы (TS DTO vs Pydantic DTO),
- единые коды ответов.

### Инструмент
- Sphinx + дополнительные источники:
  - основной упор — автогенерация из docstring роутов/функций.
  - можно дополнять “manual section” в docs/ (например, таблицей endpoints).

---

## 10.3.7 Backend: модели

### Что документируется
- ORM модели SQLAlchemy:
  - поля (колонки),
  - ограничения (unique, indexes),
  - связи между таблицами.
- Параллельно — Pydantic схемы:
  - DTO для вход/выход API.

### Где смотреть в коде
- ORM модели:
  - `backend/app/models/models.py`
- Pydantic схемы:
  - `backend/app/schemas/schemas.py`

### Какие модели есть в проекте (по коду)
- `User`:
  - `id`, `email` (unique/index), `name`, `password_hash`, `created_at`
- `Template`:
  - `type`, `complexity`, `structure` (JSONB), unique(type, complexity)
- `Specification`:
  - `user_id?`, `template_id?`, `title`, `content` (JSONB), `type`, `complexity`, `created_at`
- `SharedLink`:
  - `token` (unique/index), `spec_id` (FK, CASCADE), `created_at`

### Практическое назначение
- Понимание доменной модели и структуры БД.
- Помогает корректно расширять данные (новые поля/связи) и правила генерации.

### Инструмент
- Sphinx (autodoc) для python-модулей + manual схемы/диаграммы (если нужно).

---

## 10.3.8 Окружение и сборка

### Что документируется
- Переменные окружения:
  - БД (`DATABASE_URL`, параметры из compose)
  - Redis (`REDIS_URL`)
  - JWT (`JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRATION_HOURS`)
  - SMTP (хотя в текущем коде генерация ТЗ/экспорт не используют SMTP явно, переменные уже заложены)
- Docker:
  - `docker-compose.yml`
  - `backend/Dockerfile`, `frontend/Dockerfile`
  - reverse proxy `nginx/nginx.conf`
- Миграции:
  - Alembic (`backend/alembic/env.py` и `versions/*`)
  - входной шаг при старте: `alembic upgrade head`
- Воспроизводимость:
  - “поднять полностью систему” одной командой.

### Где смотреть в коде
- `docker-compose.yml`
- `backend/Dockerfile`
- `backend/docker-entrypoint.sh`
- `backend/alembic/env.py`
- `backend/alembic/versions/*`

### Как стартует backend (цепочка)
1) `docker-entrypoint.sh` ждёт доступности PostgreSQL (asyncpg) и Redis (redis.asyncio)
2) выполняет миграции:
   - `alembic upgrade head`
3) запускает приложение:
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000`

---

# 10.3.9 Таблица соответствия “что документируется → инструмент”

| Раздел | Что документируется | Практическое назначение | Инструмент |
|---|---|---|---|
| Обзор проекта | Назначение системы, стек, структура репозитория | Быстрое введение нового разработчика | README.md (базовый) |
| Frontend: компоненты | React-компоненты, точки расширения | Понимание клиентской архитектуры | manual + TypeDoc (для сигнатур/типов) |
| Frontend: типы и DTO | TS-интерфейсы, запрос/ответ DTO, enums | Согласованность типов frontend/backend | TypeDoc |
| Backend: сервисы | AuthService, GeneratorService, ExportService, RedisService | Сопровождение/расширение бизнес-логики | Sphinx |
| Backend: API-маршруты | FastAPI роуты, параметры, коды ответов | Интеграция frontend/backend без расхождений | Sphinx + manual endpoints |
| Backend: модели | SQLAlchemy модели, Pydantic схемы, связи таблиц | Понимание доменной модели и БД | Sphinx (+ manual описание) |
| Окружение и сборка | env vars, Docker, миграции, запуск | Воспроизводимость локального окружения | README.md / docs/ (manual) |

---

# 10.3.10 Рекомендации по унификации комментирования под автогенерацию

## Frontend (TypeDoc / JSDoc)
- Для public функций в `frontend/src/services/api.ts` добавлять JSDoc:
  - назначение,
  - параметры,
  - возвращаемое значение,
  - возможные ошибки (опционально).

## Backend (Sphinx / Google-style docstring)
- Для каждой функции сервиса и ключевых роутов:
  - единообразный формат docstring:
    - `Args:`
    - `Returns:`
    - `Raises:`
- Для методов, участвующих в экспорт/генерации:
  - описать входные `Dict[str, Any]` поля (минимум: что ожидается в `specification`).

Пример (Backend):
```py
def generate_pdf(specification: Dict[str, Any], title: str) -> bytes:
    """
    Генерирует PDF документ по структуре ТЗ.

    Args:
        specification: структура ТЗ (goal/description/requirements/etc.)
        title: заголовок документа

    Returns:
        bytes с PDF данными.

    Raises:
        (если нужно — описать исключения)
    """
    ...
