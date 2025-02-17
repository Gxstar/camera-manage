# api/lenses/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.lens_schema import Lens, LensCreate, LensUpdate
from models.database import db
from schemas.user_schema import TokenData
from api.users.routes import get_current_user

router = APIRouter()

async def check_admin_role(current_user: TokenData = Depends(get_current_user)):
    """检查当前用户是否是管理员"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return True

@router.get("/", response_model=List[Lens])
async def get_lenses():
    """获取所有镜头 (所有人)"""
    query = "SELECT * FROM lenses"
    lenses = db.fetchall(query)
    return lenses

@router.get("/{lens_id}", response_model=Lens)
async def get_lens(lens_id: int):
    """获取单个镜头 (所有人)"""
    query = "SELECT * FROM lenses WHERE id = %s"
    lens = db.fetchone(query, (lens_id,))
    if lens is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lens not found")
    return lens

@router.post("/", response_model=Lens, dependencies=[Depends(check_admin_role)])
async def create_lens(lens: LensCreate):
    """创建镜头 (仅管理员)"""
    query = """
        INSERT INTO lenses (brand_id, model, mount, min_focal_length, max_focal_length, max_aperture, min_aperture, price, release_date, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (lens.brand_id, lens.model, lens.mount, lens.min_focal_length, lens.max_focal_length, lens.max_aperture, lens.min_aperture, lens.price, lens.release_date, lens.image_url)
    db.execute(query, values)

    query = "SELECT LAST_INSERT_ID()"
    lens_id = db.fetchone(query)["LAST_INSERT_ID()"]

    query = "SELECT * FROM lenses WHERE id = %s"
    new_lens = db.fetchone(query, (lens_id,))
    return new_lens

@router.put("/{lens_id}", response_model=Lens, dependencies=[Depends(check_admin_role)])
async def update_lens(lens_id: int, lens: LensUpdate):
    """更新镜头 (仅管理员)"""
    query = """
        UPDATE lenses SET
            brand_id = %s,
            model = %s,
            mount = %s,
            min_focal_length = %s,
            max_focal_length = %s,
            max_aperture = %s,
            min_aperture = %s,
            price = %s,
            release_date = %s,
            image_url = %s
        WHERE id = %s
    """
    values = (lens.brand_id, lens.model, lens.mount, lens.min_focal_length, lens.max_focal_length, lens.max_aperture, lens.min_aperture, lens.price, lens.release_date, lens.image_url, lens_id)
    db.execute(query, values)

    query = "SELECT * FROM lenses WHERE id = %s"
    updated_lens = db.fetchone(query, (lens_id,))
    if updated_lens is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lens not found")
    return updated_lens

@router.delete("/{lens_id}", dependencies=[Depends(check_admin_role)])
async def delete_lens(lens_id: int):
    """删除镜头 (仅管理员)"""
    query = "DELETE FROM lenses WHERE id = %s"
    db.execute(query, (lens_id,))
    return {"message": "Lens deleted successfully"}
