# api/brands/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.brand import Brand, BrandCreate, BrandUpdate  # 导入 Pydantic 模型
from schemas.brand import Brand as BrandSQL  # 导入 SQLAlchemy 模型
from schemas.user import TokenData
from api.users.routes import get_current_user  # 确保路径正确
from sqlalchemy.orm import Session
from models.database import get_db

router = APIRouter()

async def check_admin_role(current_user: TokenData = Depends(get_current_user)):
    """检查当前用户是否是管理员"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return True

@router.get("/", response_model=List[Brand])
async def get_brands(db: Session = Depends(get_db)):
    """获取所有品牌 (所有人)"""
    brands = db.query(BrandSQL).all()
    return [Brand.model_validate(brand) for brand in brands]  # 转换为 Pydantic 模型

@router.get("/{brand_id}", response_model=Brand)
async def get_brand(brand_id: int, db: Session = Depends(get_db)):
    """获取单个品牌 (所有人)"""
    brand = db.query(BrandSQL).filter(BrandSQL.id == brand_id).first()
    if brand is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return Brand.model_validate(brand)  # 转换为 Pydantic 模型

@router.post("/", response_model=Brand, dependencies=[Depends(check_admin_role)])
async def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    """创建品牌 (仅管理员)"""
    db_brand = BrandSQL(**brand.dict())  # 使用 Pydantic 模型的数据创建 SQLAlchemy 对象
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return Brand.model_validate(db_brand)  # 转换为 Pydantic 模型

@router.put("/{brand_id}", response_model=Brand, dependencies=[Depends(check_admin_role)])
async def update_brand(brand_id: int, brand: BrandUpdate, db: Session = Depends(get_db)):
    """更新品牌 (仅管理员)"""
    db_brand = db.query(BrandSQL).filter(BrandSQL.id == brand_id).first()
    if db_brand is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    # 更新字段
    for key, value in brand.dict(exclude_unset=True).items():  # 仅更新已提供的字段
        setattr(db_brand, key, value)

    db.commit()
    db.refresh(db_brand)
    return Brand.model_validate(db_brand)  # 转换为 Pydantic 模型

@router.delete("/{brand_id}", dependencies=[Depends(check_admin_role)])
async def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    """删除品牌 (仅管理员)"""
    db_brand = db.query(BrandSQL).filter(BrandSQL.id == brand_id).first()
    if db_brand is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    db.delete(db_brand)
    db.commit()
    return {"message": "Brand deleted successfully"}
