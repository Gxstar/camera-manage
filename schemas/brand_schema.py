from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandBase(BaseModel):
    brand_name_en: str
    brand_name_zh: str
    logo_url: Optional[str] = None
    official_website: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BrandUpdate(BaseModel):
    brand_name_en: Optional[str] = None
    brand_name_zh: Optional[str] = None
    logo_url: Optional[str] = None
    official_website: Optional[str] = None
