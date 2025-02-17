# api/users/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from schemas.user_schema import User, UserCreate, UserUpdate, TokenData
from models.database import db
import bcrypt
from datetime import timedelta
from utils.jwt_utils import create_access_token, decode_access_token, get_password_hash, verify_password  # 导入 JWT 相关函数
from utils.config import settings

router = APIRouter()

# 创建 JWT Token 的路由
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录，获取 JWT Token"""
    username = form_data.username
    password = form_data.password

    # 查询用户
    query = "SELECT * FROM users WHERE username = %s"
    user = db.fetchone(query, (username,))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证密码
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建 JWT Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires,
        secret_key=settings.SECRET_KEY  # 传递 secret_key
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 修改 get_current_user 函数
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token"))): # 修改tokenUrl
    """从 JWT Token 中获取当前用户"""
    payload = decode_access_token(token, secret_key=settings.SECRET_KEY)  # 传递 secret_key
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    role: str = payload.get("role")
    if username is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = TokenData(username=username, role=role)
    return token_data


#  **将 check_admin_role 函数移动到这里**
async def check_admin_role(current_user: TokenData = Depends(get_current_user)):
    """检查当前用户是否是管理员"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return True


@router.get("/", response_model=List[User])
async def get_users():
    """获取所有用户"""
    query = "SELECT * FROM users"
    users = db.fetchall(query)
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """获取单个用户"""
    query = "SELECT * FROM users WHERE id = %s"
    user = db.fetchone(query, (user_id,))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=User, dependencies=[Depends(check_admin_role)])
async def create_user(user: UserCreate):
    """创建用户 (仅管理员)"""
    # 密码哈希
    hashed_password = get_password_hash(user.password)
    query = """
        INSERT INTO users (username, email, password_hash, role, token)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        user.username,
        user.email,
        hashed_password,
        user.role,
        None,
    )
    db.execute(query, values)
    # 获取新创建的用户的 ID
    query = "SELECT LAST_INSERT_ID()"
    user_id = db.fetchone(query)["LAST_INSERT_ID()"]

    # 查询新创建的用户数据并返回
    query = "SELECT * FROM users WHERE id = %s"
    new_user = db.fetchone(query, (user_id,))
    return new_user


@router.put("/{user_id}", response_model=User, dependencies=[Depends(check_admin_role)])
async def update_user(user_id: int, user: UserUpdate):
    """更新用户 (仅管理员)"""
    # 检查是否有新密码要更新
    if user.password:
        # 对新密码进行哈希处理
        hashed_password = get_password_hash(user.password)
    else:
        # 如果没有新密码，则保持原密码不变
        # 获取当前用户的密码哈希
        query = "SELECT password_hash FROM users WHERE id = %s"
        existing_user = db.fetchone(query, (user_id,))
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        hashed_password = existing_user["password_hash"]

    query = """
        UPDATE users SET
            username = %s,
            email = %s,
            password_hash = %s,
            role = %s,
            token = %s
        WHERE id = %s
    """
    values = (
        user.username,
        user.email,
        hashed_password,
        user.role,
        None,
        user_id,
    )
    db.execute(query, values)
    # 查询更新后的用户数据并返回
    query = "SELECT * FROM users WHERE id = %s"
    updated_user = db.fetchone(query, (user_id,))
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.delete("/{user_id}", dependencies=[Depends(check_admin_role)])
async def delete_user(user_id: int):
    """删除用户 (仅管理员)"""
    query = "DELETE FROM users WHERE id = %s"
    db.execute(query, (user_id,))
    return {"message": "User deleted successfully"}
