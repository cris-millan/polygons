## Dockerfile
#
## Usa una imagen base de Python
#FROM python:3.12
#
## Establece el directorio de trabajo dentro del contenedor
#WORKDIR /app
#
## Copia los archivos de requerimientos
#COPY requirements.txt .
#
## Instala las dependencias
#RUN pip install -r requirements.txt
#
## Copia el resto de los archivos del proyecto
#COPY . .
#
## Comando para iniciar la aplicación FastAPI
#CMD ["uvicorn", "src.main:app"]
