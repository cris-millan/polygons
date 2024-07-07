from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from src.core.database import SessionLocal
from src.models.polygon import Polygon

class PolygonRepository:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db

    def get_polygon_by_id(self, polygon_id: int):
        return self.db.query(Polygon).filter(Polygon.id == polygon_id).first()

    def get_all_polygons(self):
        return self.db.query(Polygon).all()

    def get_polygon_area(self, geometry: str, source_srid: int = 4326, target_srid: int = 3857):
        query = """
                SELECT ST_Area(ST_Transform(
                    ST_GeomFromText(:geometry, :source_srid),
                    :target_srid
                )) AS area_sq_meters
                """

        result = self.db.execute(
            text(query),
            {
                'geometry': geometry,
                'source_srid': source_srid,
                'target_srid': target_srid
            }
        ).fetchone()

        return result[0]
    def get_polygon_intersection(self, geometry: str, target_srid: int = 4326):
        query = """
        SELECT EXISTS (
            SELECT 1
            FROM polygons
            WHERE ST_Intersects(
                ST_Transform(
                    ST_GeomFromText(:geometry_to_check, :target_srid),
                    ST_SRID(polygons.geometry)
                ),
                polygons.geometry
            )
        ) AS intersect_exists
        """

        # Ejecuta la consulta cruda
        result = self.db.execute(
            text(query),
            {
                'geometry_to_check': geometry,
                'target_srid': target_srid
            }
        ).fetchone()

        # Accede al valor de 'intersect_exists' en el primer elemento de la tupla resultante
        return result[0]

    def create_polygon(self, name: str, description: str, geometry: str, area: float):
        polygon = Polygon(name=name, description=description, geometry=geometry)
        self.db.add(polygon)
        self.db.commit()
        self.db.refresh(polygon)
        return polygon

    def delete_polygon(self, polygon_id: int):
        polygon = self.db.query(Polygon).filter(Polygon.id == polygon_id)
