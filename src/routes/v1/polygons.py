from fastapi import APIRouter, UploadFile, status

from src.controllers.polygonsController import PolygonsController
from src.schema.response.polygon_response import PolygonResponse

router = APIRouter (
    prefix="/polygons",
    tags=["polygons"]
)

polygon_controller = PolygonsController()


@router.get("/", description="create polygons using a xlsx file", response_model=list[PolygonResponse])
def create_polygons_by_file():
    return polygon_controller.get_polygons()

@router.get("/{polygon_id}", status_code=status.HTTP_200_OK, response_model=PolygonResponse)
def create_polygons_by_file(polygon_id: int):
    return polygon_controller.get_polygons(polygon_id)
@router.post("/uploadfile", status_code=status.HTTP_201_CREATED)
async def create_polygons_by_file(
        file: UploadFile = UploadFile
):
    return await polygon_controller.create_polygons_by_file(file)