from pydantic import BaseModel
from geojson.geometry import Geometry

class PolygonResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    geometry: dict

    class Config:
        arbitrary_types_allowed = True
