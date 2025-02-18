from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"  # 默认用户角色

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # 更新密码时使用
    role: Optional[str] = None

class TokenData(BaseModel):
    username: str
    role: str
