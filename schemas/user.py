from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr
import re
from sqlalchemy.sql import func
from datetime import datetime

class UserBase(SQLModel):
    username: str
    email: EmailStr="test@example.com"
    role: str = "user"
    avatar: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @classmethod
    def validate_password(cls, value):
        # 密码强度规则：至少 8 个字符，包含至少一个大写字母、一个小写字母和一个数字
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        if not re.match(pattern, value):
            raise ValueError('密码必须至少 8 个字符长，并且包含至少一个大写字母、一个小写字母和一个数字。')
        return value

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    avatar: Optional[str] = None

    @classmethod
    def validate_password(cls, value):
        if value is not None:
            # 密码强度规则：至少 8 个字符，包含至少一个大写字母、一个小写字母和一个数字
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
            if not re.match(pattern, value):
                raise ValueError('密码必须至少 8 个字符长，并且包含至少一个大写字母、一个小写字母和一个数字。')
        return value

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    password: str
    token: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', role='{self.role}')>"

class TokenData(SQLModel):
    username: str
    role: str

