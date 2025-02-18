import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator

# 从环境变量获取数据库配置 (推荐)
DB_USER = os.environ.get("DB_USER", "camera_lens")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "gx19930804")
DB_HOST = os.environ.get("DB_HOST", "193.112.82.102")
DB_PORT = os.environ.get("DB_PORT", "3306")  # 获取端口，默认为 3306
DB_NAME = os.environ.get("DB_NAME", "camera_lens")

# 构建数据库连接字符串
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建 SQLAlchemy 引擎
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 创建 SessionLocal 类，用于创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# (可选) 创建所有表
# from .models import Base
# Base.metadata.create_all(bind=engine)
