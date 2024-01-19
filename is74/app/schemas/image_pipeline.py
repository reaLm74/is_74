from fastapi import UploadFile, File
from pydantic import BaseModel


# Класс для хранения изображения и пайплайна
class ImagePipeline(BaseModel):
    image: UploadFile = File(...)
    pipeline_id: int
