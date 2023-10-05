from fastapi import status
from src.exceptions import AppException


class TokenExpiredException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
