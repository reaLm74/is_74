from app.models.box import BoxTable
from app.utils.repository import SQLAlchemyRepository


class BoxesRepository(SQLAlchemyRepository):
    model = BoxTable
