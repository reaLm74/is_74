from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from app.api.dependencies import boxes_service
from app.api.dependencies import pipeline_service
from app.schemas.image_pipeline import ImagePipeline
from app.services.boxes import BoxesService
from app.services.pipeline import PipelineService

router = APIRouter(
    prefix="",
    tags=["Pipeline"],
)


@router.post("/process_image", status_code=status.HTTP_201_CREATED)
async def process_image(
        image_pipeline: ImagePipeline = Depends(),
        pipeline_services: PipelineService = Depends(pipeline_service),
        boxes_services: BoxesService = Depends(boxes_service)
):
    try:
        image = image_pipeline.image
        pipeline_id = image_pipeline.pipeline_id
        # Получаем пайплайн из базы данных по id
        pipeline_obj = await pipeline_services.get_pipeline(pipeline_id)
        # Обработка изображения
        image = await pipeline_services.image_processing(image, pipeline_obj)
        # Прогон обработанного изображения через модель машинного обучения
        boxes = await pipeline_services.machine_learning(image, pipeline_obj)
        if not boxes:
            return {"detail": {"status": "Car not found in image"}}
        # Сохранение в БД информации
        await boxes_services.saving_information(boxes, pipeline_obj)
        return {"detail": {"status": "Successful"}}
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "Not successful"}
        )
