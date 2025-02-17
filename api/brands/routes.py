# api/brands/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.brand_schema import Brand, BrandCreate, BrandUpdate
from models.database import db  # 确保指向你的数据库连接
from schemas.user_schema import TokenData
from api.users.routes import get_current_user  # 确保路径正确

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
async def get_brands():
    """获取所有品牌 (所有人)"""
    query = "SELECT * FROM brands"
    brands = db.fetchall(query)
    return brands

@router.get("/{brand_id}", response_model=Brand)
async def get_brand(brand_id: int):
    """获取单个品牌 (所有人)"""
    query = "SELECT * FROM brands WHERE id = %s"
    brand = db.fetchone(query, (brand_id,))
    if brand is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return brand

@router.post("/", response_model=Brand, dependencies=[Depends(check_admin_role)])
async def create_brand(brand: BrandCreate):
    """创建品牌 (仅管理员)"""
    query = """
        INSERT INTO brands (brand_name_en, brand_name_zh, logo_url, official_website)
        VALUES (%s, %s, %s, %s)
    """
    values = (brand.brand_name_en, brand.brand_name_zh, brand.logo_url, brand.official_website)
    db.execute(query, values)

    query = "SELECT LAST_INSERT_ID()"
    brand_id = db.fetchone(query)["LAST_INSERT_ID()"]

    query = "SELECT * FROM brands WHERE id = %s"
    new_brand = db.fetchone(query, (brand_id,))
    return new_brand

@router.put("/{brand_id}", response_model=Brand, dependencies=[Depends(check_admin_role)])
async def update_brand(brand_id: int, brand: BrandUpdate):
    """更新品牌 (仅管理员)"""
    query = """
        UPDATE brands SET
            brand_name_en = %s,
            brand_name_zh = %s,
            logo_url = %s,
            official_website = %s
        WHERE id = %s
    """
    values = (brand.brand_name_en, brand.brand_name_zh, brand.logo_url, brand.official_website, brand_id)
    db.execute(query, values)

    query = "SELECT * FROM brands WHERE id = %s"
    updated_brand = db.fetchone(query, (brand_id,))
    if updated_brand is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return updated_brand

@router.delete("/{brand_id}", dependencies=[Depends(check_admin_role)])
async def delete_brand(brand_id: int):
    """删除品牌 (仅管理员)"""
    query = "DELETE FROM brands WHERE id = %s"
    db.execute(query, (brand_id,))
    return {"message": "Brand deleted successfully"}
