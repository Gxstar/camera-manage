from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.sql import func
from sqlalchemy import DateTime,Column

class BrandBase(SQLModel):
    brand_name_en: str
    brand_name_zh: str
    logo_url: Optional[str] = None
    official_website: Optional[str] = None

class BrandCreate(BrandBase):
    pass

class BrandUpdate(SQLModel):
    brand_name_en: Optional[str] = None
    brand_name_zh: Optional[str] = None
    logo_url: Optional[str] = None
    official_website: Optional[str] = None

class Brand(BrandBase, table=True):
    __tablename__ = "brands"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column("created_at", DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column("updated_at", DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    )
    # 使用字符串引用 Camera 和 Lens 模型
    # cameras: List["Camera"] = Relationship(back_populates="brand")
    # lenses: List["Lens"] = Relationship(back_populates="brand")

    def __repr__(self):
        return f"<Brand(brand_name_en='{self.brand_name_en}', brand_name_zh='{self.brand_name_zh}')>"

# 在文件末尾导入其他模型，避免循环导入
from .camera import Camera
from .lens import Lens