from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, datetime
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Column  # 导入 Column

class CameraBase(SQLModel):
    brand_id: int
    model: str
    format: Optional[str] = None
    weight: Optional[float] = None
    mount: Optional[str] = None
    price: Optional[float] = None
    pixel_resolution: Optional[str] = None
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class CameraCreate(CameraBase):
    pass

class CameraUpdate(SQLModel):
    brand_id: Optional[int] = None
    model: Optional[str] = None
    format: Optional[str] = None
    weight: Optional[float] = None
    mount: Optional[str] = None
    price: Optional[float] = None
    pixel_resolution: Optional[str] = None
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class Camera(CameraBase, table=True):
    __tablename__ = "cameras"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    # 使用 Column 来定义 created_at 和 updated_at 字段
    created_at: Optional[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Optional[datetime] = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # 使用字符串引用 Brand 模型
    # brand: "Brand" = Relationship(back_populates="cameras")

    def __repr__(self):
        return f"<Camera(model='{self.model}', brand_id={self.brand_id})>"

# 在文件末尾导入 Brand 模型，避免循环导入
from .brand import Brand
