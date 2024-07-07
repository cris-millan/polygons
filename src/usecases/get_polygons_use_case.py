from src.repositories.polygon_repository import PolygonRepository
from src.schema.response.polygon_response import PolygonResponse
from src.usecases.base_use_case import BaseUseCase
from geoalchemy2.shape import to_shape

class GetPolygonsUseCase(BaseUseCase):
    def __init__(self, polygon_repository: PolygonRepository):
        self.polygon_repository = polygon_repository

    def execute(self, data):

        if data["polygon_id"] is not None:
            polygon = self.polygon_repository.get_polygon_by_id(data["polygon_id"])
            return PolygonResponse(
                id=polygon.id,
                name=polygon.name,
                description=polygon.description,
                geometry=to_shape(polygon.geometry).__geo_interface__
            )


        polygons = self.polygon_repository.get_all_polygons()


        return [
            PolygonResponse(
                id=polygon.id,
                name=polygon.name,
                description=polygon.description,
                geometry=to_shape(polygon.geometry).__geo_interface__
            ) for polygon in polygons
        ]

