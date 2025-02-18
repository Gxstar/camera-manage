# schemas/lens_schema.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class LensBase(BaseModel):
    brand_id: int
    model: str
    mount: Optional[str] = None
    min_focal_length: Optional[float] = None
    max_focal_length: Optional[float] = None
    max_aperture: float
    min_aperture: float
    price: float
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class LensCreate(LensBase):
    pass

class LensUpdate(BaseModel):
    brand_id: Optional[int] = None
    model: Optional[str] = None
    mount: Optional[str] = None
    min_focal_length: Optional[float] = None
    max_focal_length: Optional[float] = None
    max_aperture: Optional[float] = None
    min_aperture: Optional[float] = None
    price: Optional[float] = None
    release_date: Optional[date] = None
    image_url: Optional[str] = None

class Lens(LensBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
