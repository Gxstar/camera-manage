# api/cameras/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.camera import Camera, CameraCreate, CameraUpdate # 导入 Pydantic 模型
from schemas.camera import Camera as CameraSQL # 导入 SQLAlchemy 模型
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

@router.get("/", response_model=List[Camera])
async def get_cameras(db: Session = Depends(get_db)):
    """获取所有相机 (所有人)"""
    cameras = db.query(CameraSQL).all()
    return [Camera.model_validate(camera) for camera in cameras]

@router.get("/{camera_id}", response_model=Camera)
async def get_camera(camera_id: int, db: Session = Depends(get_db)):
    """获取单个相机 (所有人)"""
    camera = db.query(CameraSQL).filter(CameraSQL.id == camera_id).first()
    if camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    return Camera.model_validate(camera)

@router.post("/", response_model=Camera, dependencies=[Depends(check_admin_role)])
async def create_camera(camera: CameraCreate, db: Session = Depends(get_db)):
    """创建相机 (仅管理员)"""
    db_camera = CameraSQL(**camera.model_dump())  # 创建数据库对象
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera) # 刷新以获取新创建的 ID
    return Camera.model_validate(db_camera)

@router.put("/{camera_id}", response_model=Camera, dependencies=[Depends(check_admin_role)])
async def update_camera(camera_id: int, camera: CameraUpdate, db: Session = Depends(get_db)):
    """更新相机 (仅管理员)"""
    db_camera = db.query(CameraSQL).filter(CameraSQL.id == camera_id).first()
    if db_camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")

    # 更新字段
    for key, value in camera.model_dump(exclude_unset=True).items():  # 仅更新已提供的字段
        setattr(db_camera, key, value)

    db.commit()
    db.refresh(db_camera)
    return Camera.model_validate(db_camera)

@router.delete("/{camera_id}", dependencies=[Depends(check_admin_role)])
async def delete_camera(camera_id: int, db: Session = Depends(get_db)):
    """删除相机 (仅管理员)"""
    db_camera = db.query(CameraSQL).filter(CameraSQL.id == camera_id).first()
    if db_camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")

    db.delete(db_camera)
    db.commit()
    return {"message": "Camera deleted successfully"}
