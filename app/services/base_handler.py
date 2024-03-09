from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import DonationCRUD
from app.crud.project import CharityProjectCRUD
from app.models import CharityProject, Donation, User
from app.schemas.donation import DonationBase
from app.schemas.project import CharityProjectCreate
from app.services import constants as const
from app.services.investment import Investment


class BaseHandler:
    """
    Базовый класс для работы с данными
    """
    CRUD: Union[CharityProjectCRUD, DonationCRUD] = None

    def __init__(self, session: AsyncSession, user: User = None) -> None:
        self.session = session
        self.user = user

    async def get_all_objects_from_db(
        self,
    ) -> list[Union[CharityProject, Donation]]:
        """
        Возвращает все объекты из базы данных
        """
        if self.CRUD is None:
            raise NotImplementedError(const.DEFINE_CONSTANT)
        return await self.CRUD.get_multi(self.session)

    async def create_object(
        self, object_in: Union[CharityProjectCreate, DonationBase]
    ) -> Union[CharityProject, Donation]:
        """
        Создает новый объект
        """
        if self.CRUD is None:
            raise NotImplementedError(const.DEFINE_CONSTANT)
        new_object = await self.CRUD.create(object_in, self.session)
        investing_routine = Investment(new_object, self.session)
        return await investing_routine.money_distribution()
