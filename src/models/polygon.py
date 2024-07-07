from sqlalchemy import Column, Integer, String, Float
from src.core.database import Base
from geoalchemy2 import Geometry

class Polygon(Base):
    print("LLEGUE AL POLIGONO")
    __tablename__ = "polygons"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
    geometry = Column(Geometry('POLYGON', srid=4326))
    area = Column(Float)