from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional
import re

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

    @field_validator('password')
    def validate_password(cls, value):
        # 密码强度规则：至少 8 个字符，包含至少一个大写字母、一个小写字母和一个数字
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        if not re.match(pattern, value):
            raise ValueError('密码必须至少 8 个字符长，并且包含至少一个大写字母、一个小写字母和一个数字。')
        return value

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # 更新密码时使用
    role: Optional[str] = None

    @field_validator('password')
    def validate_password(cls, value):
        if value is not None:
            # 密码强度规则：至少 8 个字符，包含至少一个大写字母、一个小写字母和一个数字
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
            if not re.match(pattern, value):
                raise ValueError('密码必须至少 8 个字符长，并且包含至少一个大写字母、一个小写字母和一个数字。')
        return value

class TokenData(BaseModel):
    username: str
    role: str
