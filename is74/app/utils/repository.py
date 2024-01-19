import base64
from abc import ABC, abstractmethod
from random import randint, uniform

import cv2
import numpy as np
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db.db import async_session_maker
from app.models.box import BoxTable
from app.schemas.image_pipeline import ImagePipeline
from app.schemas.pipeline import PipelineSchema


class AbstractRepository(ABC):
    @abstractmethod
    async def get_pipeline(self, pipeline_id: int):
        raise NotImplementedError

    @abstractmethod
    async def image_processing(self, image, pipeline):
        raise NotImplementedError

    @abstractmethod
    async def machine_learning(self, image, pipeline):
        raise NotImplementedError

    @abstractmethod
    async def saving_information(self, boxes, pipeline):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_pipeline(self, pipeline_id: int) -> PipelineSchema:
        try:
            async with async_session_maker() as session:
                request_db = select(self.model).where(
                    self.model.id == pipeline_id
                )
                result = await session.execute(request_db)
                pipeline_table = result.scalar_one()
            # Если пайплайн найден, то преобразуем его в объект класса Pipeline
            pipeline = self.model(
                id=pipeline_table.id,
                steps_processing=pipeline_table.steps_processing.split(","),
                steps_learning=pipeline_table.steps_learning.split(","),
                steps_saving=pipeline_table.steps_saving.split(","),
            )
            return pipeline
        except SQLAlchemyError as error:
            raise Exception(
                f'Error SQLAlchemyError in get pipeline: {error}'
            )
        except Exception as error:
            raise Exception(f'Error in get pipeline: {error}')

    async def image_processing(
            self, image: ImagePipeline, pipeline: PipelineSchema
    ) -> str:
        try:
            image = np.frombuffer(await image.read(), np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            # Прогоняем изображение по шагам обработки изображения
            for step in pipeline.steps_processing:
                if step == "resize":
                    image = cv2.resize(image, (640, 640))
                elif step == "normalize":
                    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
                elif step == "base64":
                    _, image = cv2.imencode('.png', image)
                    image = base64.b64encode(image).decode()
                else:
                    raise Exception(f'Unknown step in image processing: {step}')
            return image
        except Exception as error:
            raise Exception(f'Error in image processing: {error}')

    async def machine_learning(
            self, image: str, pipeline: PipelineSchema
    ) -> BoxTable or bool:
        try:
            # Прогон обработанного изображения по шагам машинного обучения
            for _ in pipeline.steps_learning:
                pass
            if randint(0, 1):
                return False
            boxes = BoxTable(
                top_left_x=randint(0, 320),
                top_left_y=randint(0, 320),
                w=randint(0, 320),
                h=randint(0, 320),
                conf=round(uniform(0, 1), 2),
                label='1'
            )
            return boxes
        except Exception as error:
            raise Exception(f'Error in machine learning: {error}')

    async def saving_information(
            self, boxes: BoxTable, pipeline: PipelineSchema
    ) -> None:
        try:
            # Прогон обработанного изображения по шагам сохранения в БД
            for _ in pipeline.steps_saving:
                pass
            async with async_session_maker() as session:
                async with session.begin():
                    session.add(boxes)
                    await session.flush()
        except SQLAlchemyError as error:
            raise Exception(
                f'Error SQLAlchemyError in saving information: {error}'
            )
        except Exception as error:
            raise Exception(f'Error in saving information: {error}')
