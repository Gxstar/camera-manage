# admin.py
from sqladmin import Admin, ModelView
from schemas.brand_schema import Brand as BrandSQL  # 导入 SQLAlchemy 模型
from schemas.camera_schema import Camera as CameraSQL
from schemas.lens_schema import Lens as LensSQL
from schemas.user_schema import User as UserSQL


# 定义 Brand 的 ModelView
class BrandAdmin(ModelView, model=BrandSQL):
    column_list = [BrandSQL.id, BrandSQL.brand_name_en, BrandSQL.brand_name_zh]  # 显示的列
    column_searchable_list = [BrandSQL.brand_name_en, BrandSQL.brand_name_zh]  # 可以搜索的列
    column_sortable_list = [BrandSQL.id, BrandSQL.brand_name_en]  # 可以排序的列
    column_labels = {
        BrandSQL.id: "ID",
        BrandSQL.brand_name_en: "Brand Name (EN)",
        BrandSQL.brand_name_zh: "Brand Name (ZH)",
    }

# 定义 Camera 的 ModelView
class CameraAdmin(ModelView, model=CameraSQL):
    column_list = [CameraSQL.id, CameraSQL.model, CameraSQL.brand_id, CameraSQL.price]
    column_searchable_list = [CameraSQL.model]
    column_sortable_list = [CameraSQL.id, CameraSQL.model, CameraSQL.price]
    column_labels = {
        CameraSQL.id: "ID",
        CameraSQL.model: "Model",
        CameraSQL.brand_id: "Brand ID",
        CameraSQL.price: "Price",
    }

# 定义 Lens 的 ModelView
class LensAdmin(ModelView, model=LensSQL):
    column_list = [LensSQL.id, LensSQL.model, LensSQL.brand_id, LensSQL.price]
    column_searchable_list = [LensSQL.model]
    column_sortable_list = [LensSQL.id, LensSQL.model, LensSQL.price]
    column_labels = {
        LensSQL.id: "ID",
        LensSQL.model: "Model",
        LensSQL.brand_id: "Brand ID",
        LensSQL.price: "Price",
    }

class UserAdmin(ModelView, model=UserSQL):
    column_list = [UserSQL.id, UserSQL.username, UserSQL.email, UserSQL.role]
    column_searchable_list = [UserSQL.username, UserSQL.email]
    column_sortable_list = [UserSQL.id, UserSQL.username, UserSQL.email, UserSQL.role]
    column_labels = {
        UserSQL.id: "ID",
        UserSQL.username: "Username",
        UserSQL.email: "Email",
        UserSQL.role: "Role",
    }

