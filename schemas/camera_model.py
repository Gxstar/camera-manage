# schemas/camera_schema.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class CameraBase(BaseModel):
    brand_id: int
    model: str
    format: Optional[str] = None
    weight: Optional[float] = None
    mount: Optional[str] = None
    price: Optional[float] = None
    pixel_resolution: Optional[str] = None
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class CameraCreate(CameraBase):
    pass

class CameraUpdate(BaseModel):
    brand_id: Optional[int] = None
    model: Optional[str] = None
    format: Optional[str] = None
    weight: Optional[float] = None
    mount: Optional[str] = None
    price: Optional[float] = None
    pixel_resolution: Optional[str] = None
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class Camera(CameraBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
