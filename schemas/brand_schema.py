from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand_name_en = Column(String(255), nullable=False, unique=True)  # 英文名，非空，唯一
    brand_name_zh = Column(String(255), nullable=False)  # 中文名，非空
    logo_url = Column(String(255), nullable=True)  # Logo URL，可为空
    official_website = Column(String(255), nullable=True)  # 官网 URL，可为空
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间，自动生成
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # 更新时间，自动更新

    def __repr__(self):
        return f"<Brand(brand_name_en='{self.brand_name_en}', brand_name_zh='{self.brand_name_zh}')>"
