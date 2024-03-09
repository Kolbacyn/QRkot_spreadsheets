from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_project_exists, check_project_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.project import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.services.project import CharityProjectHandler

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создание благотворительного проекта.'
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для суперпользователей.

    Создает благотворительный проект.
    """
    await check_project_name_duplicate(project.name, session)
    project_handler = CharityProjectHandler(session)
    return await project_handler.create_charity_project(
        project
    )


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Просмотреть все благотворительные проекты.'
)
async def get_projects(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectDB]:
    """Получает список всех проектов."""
    project_handler = CharityProjectHandler(session)
    return await project_handler.get_all_objects_from_db()


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Обновление благотворительного проекта.',
    dependencies=[Depends(current_superuser)]
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для суперпользователей.

    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    await check_project_exists(project_id, session)
    project_handler = CharityProjectHandler(session)
    return await project_handler.update_charity_project(
        project_id, obj_in
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Удаление благотворительного проекта.',
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для суперпользователей.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    await check_project_exists(project_id, session)
    project_handler = CharityProjectHandler(session)
    return await project_handler.delete_charity_project(project_id)
