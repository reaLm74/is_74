from typing import List

from pydantic import BaseModel


# Класс для хранения пайплайна обработки изображения
class PipelineSchema(BaseModel):
    id: int
    steps_processing: List[str]
    steps_learning: List[str]
    steps_saving: List[str]

    class Config:
        from_attributes = True
