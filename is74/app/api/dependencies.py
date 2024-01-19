from app.repositories.pipeline import PipelineRepository
from app.repositories.boxes import BoxesRepository
from app.services.boxes import BoxesService
from app.services.pipeline import PipelineService


def pipeline_service():
    return PipelineService(PipelineRepository)


def boxes_service():
    return BoxesService(BoxesRepository)
