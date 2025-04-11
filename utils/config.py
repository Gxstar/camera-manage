# utils/config.py
from pydantic_settings import BaseSettings,SettingsConfigDict
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()  # 默认从项目根目录加载 .env 文件

class Settings(BaseSettings):
    SECRET_KEY: str =  os.environ.get("SECRET_KEY") #  Change this to a secure random key
    ALGORITHM: str = "HS256"
    # 修改为 7 天的分钟数
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # Access token 过期时间 (分钟)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
