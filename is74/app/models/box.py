from sqlalchemy import Column, Integer, String, Float

from app.db.db import Base


# Класс для таблицы бокса
class BoxTable(Base):
    __tablename__ = "boxes"

    id = Column(Integer, primary_key=True)
    top_left_x = Column(Integer)
    top_left_y = Column(Integer)
    w = Column(Integer)
    h = Column(Integer)
    conf = Column(Float)
    label = Column(String)
