from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        closed_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(CharityProject.close_date - CharityProject.create_date)
        )
        return closed_projects.scalars().all()


charity_crud = CharityProjectCRUD(CharityProject)
