from app.models.pipeline import PipelineTable
from app.utils.repository import SQLAlchemyRepository


class PipelineRepository(SQLAlchemyRepository):
    model = PipelineTable
