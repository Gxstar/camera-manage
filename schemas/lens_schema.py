from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Lens(Base):
    __tablename__ = "lenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)  # 外键，关联到 brands 表
    model = Column(String(255), nullable=False)  # 型号，非空
    mount = Column(String(255), nullable=True)  # 卡口，可为空
    min_focal_length = Column(Float, nullable=True)  # 最小焦距，可为空
    max_focal_length = Column(Float, nullable=True)  # 最大焦距，可为空
    max_aperture = Column(Float, nullable=False)  # 最大光圈，非空
    min_aperture = Column(Float, nullable=False)  # 最小光圈，非空
    price = Column(Float, nullable=False)  # 价格，非空
    release_date = Column(Date, nullable=True)  # 发布日期，可为空
    image_url = Column(String(255), nullable=True)  # 图片 URL，可为空
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间，自动生成
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # 更新时间，自动更新

    # 定义与 Brand 模型的关联关系
    brand = relationship("Brand", backref="lenses")  # backref 允许从 Brand 模型反向查询 Lenses

    def __repr__(self):
        return f"<Lens(model='{self.model}', brand_id={self.brand_id})>"
