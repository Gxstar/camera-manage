# api/lenses/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.lens import Lens, LensCreate, LensUpdate  # 导入 Pydantic 模型
from schemas.lens import Lens as LensSQL  # 导入 SQLAlchemy 模型
from schemas.user import TokenData
from api.users.routes import get_current_user
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

@router.get("/", response_model=List[Lens])
async def get_lenses(db: Session = Depends(get_db)):
    """获取所有镜头 (所有人)"""
    lenses = db.query(LensSQL).all()
    return [Lens.model_validate(lens) for lens in lenses]

@router.get("/{lens_id}", response_model=Lens)
async def get_lens(lens_id: int, db: Session = Depends(get_db)):
    """获取单个镜头 (所有人)"""
    lens = db.query(LensSQL).filter(LensSQL.id == lens_id).first()
    if lens is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lens not found")
    return Lens.model_validate(lens)

@router.post("/", response_model=Lens, dependencies=[Depends(check_admin_role)])
async def create_lens(lens: LensCreate, db: Session = Depends(get_db)):
    """创建镜头 (仅管理员)"""
    db_lens = LensSQL(**lens.model_dump())  # 创建数据库对象
    db.add(db_lens)
    db.commit()
    db.refresh(db_lens)  # 刷新以获取新创建的 ID
    return Lens.model_validate(db_lens)

@router.put("/{lens_id}", response_model=Lens, dependencies=[Depends(check_admin_role)])
async def update_lens(lens_id: int, lens: LensUpdate, db: Session = Depends(get_db)):
    """更新镜头 (仅管理员)"""
    db_lens = db.query(LensSQL).filter(LensSQL.id == lens_id).first()
    if db_lens is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lens not found")

    # 更新字段
    for key, value in lens.model_dump(exclude_unset=True).items():  # 仅更新已提供的字段
        setattr(db_lens, key, value)

    db.commit()
    db.refresh(db_lens)
    return Lens.model_validate(db_lens)

@router.delete("/{lens_id}", dependencies=[Depends(check_admin_role)])
async def delete_lens(lens_id: int, db: Session = Depends(get_db)):
    """删除镜头 (仅管理员)"""
    db_lens = db.query(LensSQL).filter(LensSQL.id == lens_id).first()
    if db_lens is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lens not found")

    db.delete(db_lens)
    db.commit()
    return {"message": "Lens deleted successfully"}
