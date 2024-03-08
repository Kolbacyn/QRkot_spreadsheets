from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_project_exists
from app.crud.project import charity_crud
from app.models.charity_project import CharityProject
from app.schemas.project import CharityProjectUpdate
from app.services import constants as const


async def check_project_name_duplicate(
    name: str,
    session: AsyncSession,
):
    project_id = await charity_crud.get_project_id_by_name(
        name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=const.PROJECT_NAME_EXISTS,
        )


async def check_project_before_delete(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка проекта перед удалением"""
    await check_project_exists(project_id, session)
    project = await charity_crud.get(project_id, session)
    if project.invested_amount > const.TOTAL_ZERO:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=const.PROJECT_HAS_DONATIONS,
        )
    return project


async def check_project_if_close(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """
    Проверка не закрыт ли проект
    """
    project = await charity_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=const.PROJECT_CLOSED
        )

    return project


async def check_project_before_update(
    project_id: int, session: AsyncSession, obj_in: CharityProjectUpdate
) -> CharityProject:
    """Прверка проекта перед обновлением"""
    await check_project_exists(project_id, session)
    if obj_in.name:
        await check_project_name_duplicate(obj_in.name, session)
    project = await check_project_if_close(project_id, session)
    if obj_in.full_amount:
        if project.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=const.TOTAL_SHOULD_BE_GREATER_THAN_INVESTED,
            )
    return project
