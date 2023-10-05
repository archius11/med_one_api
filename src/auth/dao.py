

from src.database.base import async_session_maker
from src.auth.models import User
from src.database.base import BaseDAO


class UserDAO(BaseDAO):
    model = User
