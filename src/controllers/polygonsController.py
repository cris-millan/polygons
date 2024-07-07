from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from src.core.exceptions import UnprocessableEntityError, BadRequestError, InternalServerError
from src.repositories.polygon_repository import PolygonRepository
from src.usecases.create_polygons_by_file_use_case import CreatePolygonsByFileUseCase
from src.usecases.get_polygons_use_case import GetPolygonsUseCase

import pandas as pd

from io import BytesIO



XLSX_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
XLSX_EXTENSION = 'xlsx'
class PolygonsController:


    def __init__(self):
        self.file_repository = PolygonRepository()
        self.create_polygons_by_file_use_case = CreatePolygonsByFileUseCase(self.file_repository)
        self.get_polygons_use_case = GetPolygonsUseCase(self.file_repository)

    def getVertices(self, coord_string):

        # split geometry in points
        points = coord_string.split(',')

        #validate pints must be have 3  and have to be pairs.
        if len(points) < 6 or len(points) % 2 != 0:
            raise BadRequestError(
                detail={
                    "code": "POL-11-04",
                    "description": "geometry field must have more than 3 segments and each segment need have 22 points"
                })

        # group los points on tuples of two elements
        vertices = [(float(points[i]), float(points[i + 1])) for i in range(0, len(points), 2)]

        return vertices

    def get_polygons(self, polygon_id: int = None):
        return self.get_polygons_use_case.execute({"polygon_id": polygon_id})

    async def create_polygons_by_file(self, file: UploadFile):
        # take file name
        filename = file.filename
        # get file extension after .
        extension = filename.split('.')[-1]
        #validate file extension and content type
        if extension == '' or extension != XLSX_EXTENSION or file.content_type != XLSX_CONTENT_TYPE:
            raise HTTPException(status_code=400, detail="extension must be .xlsx or .xlsx ")

        # TODO validate file size

        #read file
        contents = await file.read()

        #validate fie
        if not contents:
            raise BadRequestError(
                detail={
                    "code": "POL-11-01",
                    "errors": "the file is empty"
                })
        #create data frame
        try:
            df = pd.read_excel(BytesIO(contents))
        except Exception as e:
            raise InternalServerError(
                detail={
                    "code": "POL-11-02",
                    "errors": "unexpected error, error when try to read excel file"
                })

        #validate file headers
        required_columns = ['name', 'description', 'geometry']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if len(missing_columns) > 0:
            raise InternalServerError(
                detail={
                    "code": "POL-11-03",
                    "errors": "The file must contain the following columns ['name', 'description', 'category']"
                })

        # cast geometry to string
        df['geometry'] = df['geometry'].astype(str)
        #cast dataframe to dict
        polygons =  df.to_dict("records")
        #cast geometry string to a list o tuples "vertices"
        for polygon in polygons:
            polygon["geometry"] = self.getVertices(polygon["geometry"])


        return self.create_polygons_by_file_use_case.execute({"polygons": polygons})

