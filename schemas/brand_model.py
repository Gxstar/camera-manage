from pydantic import BaseModel, ConfigDict
from typing import Optional

class BrandBase(BaseModel):
    brand_name_en: str
    brand_name_zh: str
    logo_url: Optional[str] = None
    official_website: Optional[str] = None

class BrandCreate(BrandBase):
    pass  # BrandCreate 模型与 BrandBase 相同

class BrandUpdate(BaseModel):
    brand_name_en: Optional[str] = None
    brand_name_zh: Optional[str] = None
    logo_url: Optional[str] = None
    official_website: Optional[str] = None

class Brand(BrandBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
