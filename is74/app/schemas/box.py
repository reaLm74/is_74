from pydantic import BaseModel


# Создаем класс для хранения координат бокса
class Box(BaseModel):
    top_left_x: int
    top_left_y: int
    w: int
    h: int
    conf: float
    label: str
