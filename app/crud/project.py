from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import datetime_func
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase):
    """
    CRUD для благотворительного проекта
    """
    async def get_project_id_by_name(
        self,
        name: str,
        session: AsyncSession
    ):
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == name)
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        query = select(
            CharityProject.name,
            CharityProject.description,
            (
                datetime_func(CharityProject.close_date) -
                datetime_func(CharityProject.create_date)
            ).label('lifetime')
        )
        query = (
            query.order_by(asc('lifetime')),
            query.order_by(desc('lifetime'))
        )[False]

        closed_projects = await session.execute(query)
        return closed_projects.all()


charity_crud = CharityProjectCRUD(CharityProject)
