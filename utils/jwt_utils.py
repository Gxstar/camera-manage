# utils/jwt_utils.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key: str = None):  # 添加 secret_key 参数
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")  # 使用 secret_key
    return encoded_jwt


def decode_access_token(token: str, secret_key: str = None) -> Optional[dict]:  # 添加 secret_key 参数
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])  # 使用 secret_key
        return payload
    except JWTError:
        return None
