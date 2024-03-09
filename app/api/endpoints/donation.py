from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.schemas.donation import (
    DonationCreate,
    DonationDB
)
from app.services import constants as const
from app.services.donation import DonationHandler

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'fully_invested', 'close_date', 'invested_amount', 'user_id'},
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: int = Depends(current_user),
) -> DonationDB:
    """
    Только для зарегистрированных пользователей.

    Создает пожертвование.
    """
    donation_handler = DonationHandler(session, user)
    new_donation = await donation_handler.create_object(
        donation
    )
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> list[DonationDB]:
    """
    Только для суперпользователя.

    Возвращает список всех пожертвований.
    """
    donation_handler = DonationHandler(session)
    return await donation_handler.get_all_objects_from_db()


@router.get(
    '/{donation_id}',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={'fully_invested', 'close_date', 'invested_amount', 'user_id'},
)
async def get_user_donations(
    user_id: int = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[DonationDB]:
    """
    Только для зарегистрированных пользователей.

    Возвращает список пожертвований пользователя.
    """
    donation_handler = DonationHandler(session, user_id)
    return await donation_handler.get_user_donations()


@router.patch(
    '/{donation_id}',
    deprecated=True
)
def update_donation(
    donation_id: int,
) -> None:
    """
    Patch-метод для обновления пожертвования.

    Не доступен для всех категорий пользователей
    """
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=const.METHOD_NOT_SUPPORTED
    )


@router.delete(
    '/{donation_id}',
    deprecated=True
)
def delete_donation(
    donation_id: int,
) -> None:
    """
    Delete-метод для удаления пожертвования.

    Не доступен для всех категорий пользователей
    """
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=const.METHOD_NOT_SUPPORTED
    )
