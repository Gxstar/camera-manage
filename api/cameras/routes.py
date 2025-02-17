# api/cameras/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.camera_schema import Camera, CameraCreate, CameraUpdate
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

@router.get("/", response_model=List[Camera])
async def get_cameras():
    """获取所有相机 (所有人)"""
    query = "SELECT * FROM cameras"
    cameras = db.fetchall(query)
    return cameras

@router.get("/{camera_id}", response_model=Camera)
async def get_camera(camera_id: int):
    """获取单个相机 (所有人)"""
    query = "SELECT * FROM cameras WHERE id = %s"
    camera = db.fetchone(query, (camera_id,))
    if camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    return camera

@router.post("/", response_model=Camera, dependencies=[Depends(check_admin_role)])
async def create_camera(camera: CameraCreate):
    """创建相机 (仅管理员)"""
    query = """
        INSERT INTO cameras (brand_id, model, format, weight, mount, price, pixel_resolution, release_date, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (camera.brand_id, camera.model, camera.format, camera.weight, camera.mount, camera.price, camera.pixel_resolution, camera.release_date, camera.image_url)
    db.execute(query, values)

    query = "SELECT LAST_INSERT_ID()"
    camera_id = db.fetchone(query)["LAST_INSERT_ID()"]

    query = "SELECT * FROM cameras WHERE id = %s"
    new_camera = db.fetchone(query, (camera_id,))
    return new_camera

@router.put("/{camera_id}", response_model=Camera, dependencies=[Depends(check_admin_role)])
async def update_camera(camera_id: int, camera: CameraUpdate):
    """更新相机 (仅管理员)"""
    query = """
        UPDATE cameras SET
            brand_id = %s,
            model = %s,
            format = %s,
            weight = %s,
            mount = %s,
            price = %s,
            pixel_resolution = %s,
            release_date = %s,
            image_url = %s
        WHERE id = %s
    """
    values = (camera.brand_id, camera.model, camera.format, camera.weight, camera.mount, camera.price, camera.pixel_resolution, camera.release_date, camera.image_url, camera_id)
    db.execute(query, values)

    query = "SELECT * FROM cameras WHERE id = %s"
    updated_camera = db.fetchone(query, (camera_id,))
    if updated_camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    return updated_camera

@router.delete("/{camera_id}", dependencies=[Depends(check_admin_role)])
async def delete_camera(camera_id: int):
    """删除相机 (仅管理员)"""
    query = "DELETE FROM cameras WHERE id = %s"
    db.execute(query, (camera_id,))
    return {"message": "Camera deleted successfully"}
