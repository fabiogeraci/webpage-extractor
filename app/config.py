from pydantic import BaseModel
import os


class Settings(BaseModel):
    base_data_dir: str = os.getenv("BASE_DATA_DIR", "/data")
    default_data_dir: str = os.getenv("DEFAULT_DATA_DIR", "/data")


settings = Settings()