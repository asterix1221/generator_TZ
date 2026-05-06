"""Custom exception classes for the application."""


class AppException(Exception):
    """Base application exception."""
    status_code: int = 500
    detail: str = "Внутренняя ошибка сервера"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class NotFoundException(AppException):
    status_code = 404
    detail = "Ресурс не найден"


class UnauthorizedException(AppException):
    status_code = 401
    detail = "Требуется авторизация"


class ForbiddenException(AppException):
    status_code = 403
    detail = "Доступ запрещен"


class BadRequestException(AppException):
    status_code = 400
    detail = "Некорректный запрос"


class ConflictException(AppException):
    status_code = 409
    detail = "Конфликт данных"


class TooManyRequestsException(AppException):
    status_code = 429
    detail = "Слишком много запросов"


class ExportException(AppException):
    status_code = 500
    detail = "Ошибка экспорта документа"


class TemplateNotFoundException(AppException):
    status_code = 404
    detail = "Шаблон не найден"