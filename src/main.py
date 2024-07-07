from fastapi import FastAPI
from src.core.config import configs
from src.core.database import engine, Base
from src.util.class_object import singleton
from src.routes.v1.routes import routers as v1_routers
from src.models.polygon import Polygon

@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )

        @self.app.get("/")
        def root():
            return {"message": f"Hello World {configs.PROJECT_NAME}"}

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)

        @self.app.on_event("startup")
        def startup():
            print("startup create all database")
            Base.metadata.create_all(bind=engine)





app_creator = AppCreator()
app = app_creator.app
