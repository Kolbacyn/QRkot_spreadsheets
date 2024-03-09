from app.api.endpoints.validators import check_project_exists
from app.crud.project import charity_crud
from app.crud.validators import check_project_before_delete, check_project_before_update
from app.models import CharityProject
from app.schemas.project import CharityProjectCreate, CharityProjectUpdate
from app.services.base_handler import BaseHandler
from app.services.investment import Investment


class CharityProjectHandler(BaseHandler):
    """
    Хэндлер для работы с проектами.
    """
    CRUD = charity_crud

    async def create_charity_project(
        self, charity_project: CharityProjectCreate
    ) -> CharityProject:
        """
        Только для суперпользователей.

        Создает проект.
        """
        return await super().create_object(charity_project)

    async def delete_charity_project(self, project_id: int) -> CharityProject:
        """
        Только для суперпользователей.

        Удаляет проект."""
        await check_project_exists(project_id, self.session)
        charity_project = await check_project_before_delete(
            project_id, self.session
        )
        return await self.CRUD.remove(charity_project, self.session)

    async def update_charity_project(
        self, project_id: int, project: CharityProjectUpdate
    ) -> CharityProject:
        """
        Только для суперпользователей.

        Изменяет проект.
        """
        charity_project = await check_project_before_update(
            project_id, self.session, project
        )
        charity_project = await self.CRUD.update(
            charity_project, project, self.session
        )
        investing_routine = Investment(charity_project, self.session)
        return await investing_routine.money_distribution()
