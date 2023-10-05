from datetime import datetime
import uuid
from pydantic import BaseModel


class LoginUserSchema(BaseModel):
    phone_number: str


class ConfirmCodeSchema(BaseModel):
    phone_number: str
    confirmation_code: str


class UserResponse(BaseModel):
    id: uuid.UUID
    phone_number: str
    role: str
    created_at: datetime
    updated_at: datetime
