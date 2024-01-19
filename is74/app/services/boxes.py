from app.utils.repository import AbstractRepository


class BoxesService:
    def __init__(self, pipeline_repo: [AbstractRepository]):
        self.pipeline_repo: AbstractRepository = pipeline_repo()

    async def saving_information(self, information, pipeline):
        result = await self.pipeline_repo.saving_information(
            information, pipeline
        )
        return result
