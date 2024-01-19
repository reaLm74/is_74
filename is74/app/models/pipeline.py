from sqlalchemy import Column, Integer, String

from app.db.db import Base


# Класс для таблицы пайплайнов
class PipelineTable(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True)
    steps_processing = Column(String)
    steps_learning = Column(String)
    steps_saving = Column(String)
