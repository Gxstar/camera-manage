from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, datetime
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Column  # 导入 Column

class LensBase(SQLModel):
    brand_id: int
    model: str
    mount: Optional[str] = None
    min_focal_length: Optional[float] = None
    max_focal_length: Optional[float] = None
    max_aperture: Optional[float] = None
    min_aperture: Optional[float] = None
    price: Optional[float] = None
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class LensCreate(LensBase):
    pass

class LensUpdate(SQLModel):
    brand_id: Optional[int] = None
    model: Optional[str] = None
    mount: Optional[str] = None
    min_focal_length: Optional[float] = None
    max_focal_length: Optional[float] = None
    max_aperture: Optional[float] = None
    min_aperture: Optional[float] = None
    price: Optional[float] = None
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class Lens(LensBase, table=True):
    __tablename__ = "lenses"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    # 使用 Column 来定义 created_at 和 updated_at 字段
    created_at: Optional[datetime] = Field(
        sa_column=Column("created_at", DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column("updated_at", DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    )
    # 使用字符串引用 Brand 模型
    # brand: "Brand" = Relationship(back_populates="lenses")

    def __repr__(self):
        return f"<Lens(model='{self.model}', brand_id={self.brand_id})>"

# 在文件末尾导入 Brand 模型，避免循环导入
from .brand import Brand