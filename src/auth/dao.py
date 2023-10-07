

from src.database.base import async_session_maker
from src.auth.models import User
from src.database.base import BaseDAO

from sqlalchemy import update


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def set_user_verified(cls, user: User):
        async with async_session_maker() as session:
            query = update(User).filter_by(id=user.id).values(verified=True)
            await session.execute(query)
            await session.commit()
