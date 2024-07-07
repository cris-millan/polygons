from src.core.exceptions import UnprocessableEntityError, BadRequestError
from src.repositories.polygon_repository import PolygonRepository
from src.usecases.base_use_case import BaseUseCase
from shapely.geometry import Polygon
from itertools import combinations


class CreatePolygonsByFileUseCase(BaseUseCase):
    def __init__(self, polygon_repository: PolygonRepository):
        self.polygon_repository = polygon_repository


    def createPoligonStatament(self, vertices):
        polygon_str = "POLYGON(("
        for coord in vertices:
            polygon_str += f"{coord[0]} {coord[1]}, "
        polygon_str += f"{vertices[0][0]} {vertices[0][1]} ))"  # add first vertice at the end to close the polygon
        # polygon_str = polygon_str[:-2]
        # polygon_str += "))"

        return polygon_str

    def validate_file_intersection(self, polygons_data) -> list:
        polygons_shaped = []
        for polygon in polygons_data:
            print(polygon["geometry"])
            geometry = self.createPoligonStatament(polygon["geometry"])
            polygons_shaped.append(Polygon(polygon["geometry"]))

        errors = []
        for poly1, poly2 in combinations(polygons_shaped, 2):
            if poly1.intersects(poly2):
                # check polygons duplicated
                if polygons_shaped.index(poly1) == polygons_shaped.index(poly2):
                    poly1_name = polygons_data[polygons_shaped.index(poly1)]['name']
                    errors.append(f"polygon {poly1_name} geometry field is duplicated in the xlsx")
                    continue

                # different polygons intersected
                # match index because have the same length
                poly1_name = polygons_data[polygons_shaped.index(poly1)]['name']
                poly2_name = polygons_data[polygons_shaped.index(poly2)]['name']
                # There are duplicates, both find the same index
                errors.append(
                    f"Polygon '{poly1_name}' intersects with polygon '{poly2_name}'")
        return errors

    def validate_db_intersection(self, polygons_data) -> list:
        errors = []
        for polygon in polygons_data:
            geometry = self.createPoligonStatament(polygon["geometry"])
            #check if polygon has intersection with polygons inventory
            if self.polygon_repository.get_polygon_intersection(geometry):
                errors.append(f"{polygon['name']} geometry has an intersection with another polygon")
        return errors


    def execute(self, data):
        #TODO create a job to do this proccess in backgroudd
        print("creating polygons by file")
        print(data)

        polygons_data = data["polygons"]

        errors = self.validate_file_intersection(polygons_data)

        if len(errors) > 0:
            raise BadRequestError(
                detail={
                    "code": "POL-21-01",
                    "errors": errors
                })
        errors = self.validate_db_intersection(polygons_data)

        if len(errors) > 0:
            raise UnprocessableEntityError(
                detail={
                    "code": "POL-22-01",
                    "errors": errors
                })

        for polygon in polygons_data:
            #create POLYGON((geometry)) sentence
            geometry = self.createPoligonStatament(polygon["geometry"])
            #generate area in m2 using database
            area = self.polygon_repository.get_polygon_area(geometry)
            self.polygon_repository.create_polygon(
                name=polygon["name"],
                description=polygon["description"],
                geometry=geometry,
                area=area
            )

        return data