import uuid
from src.database.base import BaseModel
from sqlalchemy import TIMESTAMP, Column, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    phone_number = Column(String,  nullable=False)
    name = Column(String,  nullable=True)
    last_name = Column(String,  nullable=True)
    email = Column(String, unique=True, nullable=True)
    verified = Column(Boolean, nullable=False, server_default='False')
    role = Column(String, server_default='user', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
