from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)  # 用户名，非空，唯一
    email = Column(String(255), unique=True, nullable=False)  # 邮箱，非空，唯一
    hashed_password = Column(String(255), nullable=False)  # 哈希密码，非空
    role = Column(String(50), default="user")  # 角色，默认为 "user"
    token = Column(String(255), nullable=True)  # 令牌，可为空
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间，自动生成
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # 更新时间，自动更新
    avatar = Column(String(255), nullable=True)  # 头像，可为空

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', role='{self.role}')>"
