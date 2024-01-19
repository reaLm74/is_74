from app.schemas.pipeline import PipelineSchema
from app.utils.repository import AbstractRepository
from fastapi import Depends


class PipelineService:
    def __init__(self, pipeline_repo: [AbstractRepository]):
        self.pipeline_repo: AbstractRepository = pipeline_repo()

    async def get_pipeline(self, pipeline_id: int):
        pipeline_obj = await self.pipeline_repo.get_pipeline(pipeline_id)
        return pipeline_obj

    async def image_processing(
            self, image, pipeline_obj: PipelineSchema = Depends()
    ):
        image_ready = await self.pipeline_repo.image_processing(
            image, pipeline_obj
        )
        return image_ready

    async def machine_learning(self, image, pipeline):
        coordinates = await self.pipeline_repo.machine_learning(image, pipeline)
        return coordinates
