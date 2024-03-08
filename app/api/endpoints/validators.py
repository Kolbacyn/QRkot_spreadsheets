from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import charity_crud
from app.models.charity_project import CharityProject
from app.services import constants as const


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=const.PROJECT_NOT_FOUND)
    return project


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