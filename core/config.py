import os
from typing import List

from dotenv import load_dotenv
# from pydantic import BaseSettings

load_dotenv() # take environment variables from .env.

#post gis st_intersect

class Configs():
    # Api base
    ENV: str = os.getenv("ENV", "dev")
    API: str = os.getenv("API", "dev")
    API_V1_STR: str = os.getenv("API_V1_STR", "dev")
    PROJECT_NAME: str =  os.getenv("PROJECT_NAME", "polygons-api")


    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 60 minutes * 24 hours * 30 days = 30 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # database
    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")
    DB_NAME: str = os.getenv("DB", "sinecta")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", "3306")

    DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"

    DATABASE_URI = "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
        db_engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

    class Config:
        case_sensitive = True



configs = Configs()
