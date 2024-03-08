from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.project import charity_crud
from app.schemas.project import CharityProjectDB
from app.services import google_api

router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
) -> dict[str, int]:
    """
    Только для суперпользователя.
    """
    closed_projects = await charity_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await google_api.spreadsheets_create(wrapper_services)
    await google_api.set_user_permissions(spreadsheetid, wrapper_services)
    await google_api.spreadsheets_update_value(spreadsheetid,
                                               closed_projects,
                                               wrapper_services)
    return closed_projects
