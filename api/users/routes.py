# api/users/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from schemas.user import User, UserCreate, UserUpdate, TokenData  # 导入 Pydantic 模型
import bcrypt
from datetime import timedelta
from utils.jwt_utils import create_access_token, decode_access_token, get_password_hash, verify_password  # 导入 JWT 相关函数
from utils.config import settings
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.user import User as UserModel  # 从 models 中导入 SQLAlchemy User 模型

router = APIRouter()

# 创建 JWT Token 的路由
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录，获取 JWT Token"""
    username = form_data.username
    password = form_data.password

    # 查询用户
    user = db.query(UserModel).filter(UserModel.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证密码
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建 JWT Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},  # 使用 SQLAlchemy 用户的 username 和 role
        expires_delta=access_token_expires,
        secret_key=settings.SECRET_KEY,  # 传递 secret_key
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 修改 get_current_user 函数
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")), db: Session = Depends(get_db)):
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

    token_data = TokenData(username=username, role=role)  # 直接从 payload 创建 TokenData 的 *实例*
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

@router.get("/", response_model=List[User], dependencies=[Depends(check_admin_role)])
async def get_users(db: Session = Depends(get_db)):
    """获取所有用户"""
    users = db.query(UserModel).all()
    return [User.model_validate(user) for user in users]  # 将 SQLAlchemy 模型转换为 Pydantic 模型

@router.get("/{user_id}", response_model=User, dependencies=[Depends(check_admin_role)])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取单个用户"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return User.model_validate(user)  # 将 SQLAlchemy 模型转换为 Pydantic 模型

@router.post("/", response_model=User, dependencies=[Depends(check_admin_role)])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建用户 (仅管理员)"""
    # 密码哈希
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(  # 使用 UserModel
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        token=None,  # 初始token设置为None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User.model_validate(db_user)  # 将 SQLAlchemy 模型转换为 Pydantic 模型

@router.put("/{user_id}", response_model=User, dependencies=[Depends(check_admin_role)])
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """更新用户 (仅管理员)"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 更新字段
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.role:
        db_user.role = user.role

    db.commit()
    db.refresh(db_user)
    return User.model_validate(db_user)  # 将 SQLAlchemy 模型转换为 Pydantic 模型

@router.delete("/{user_id}", dependencies=[Depends(check_admin_role)])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户 (仅管理员)"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# 新增注册 API
@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # 密码哈希
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role,
        token=None,  # 初始token设置为None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User.model_validate(db_user)