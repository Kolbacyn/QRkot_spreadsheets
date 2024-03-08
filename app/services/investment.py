from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import DonationCRUD
from app.crud.project import CharityProjectCRUD
from app.models import CharityProject, Donation


class Investment:
    """
    Класс для распределения денежных средств между проектами и пожертвованиями
    """
    def __init__(
        self,
        object: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> None:
        self.object = object
        self.session = session

    def __close_object(
        self,
        obj: Union[CharityProject, Donation]
    ) -> Union[CharityProject, Donation]:
        """
        Закрывает проект или пожертвование
        """
        obj.fully_invested = True
        obj.close_date = datetime.now()
        obj.invested_amount = obj.full_amount
        return obj

    def __get_related_class(
        self
    ) -> Union[CharityProjectCRUD, DonationCRUD]:
        """
        Возвращает CRUD-класс для проекта или пожертвования
        """
        if isinstance(self.object, Donation):
            return CharityProjectCRUD(CharityProject)
        if isinstance(self.object, CharityProject):
            return DonationCRUD(Donation)

    async def money_distribution(
        self
    ) -> Union[CharityProject, Donation]:
        """
        Распределяет деньги между проектами и пожертвованиями
        """
        obj = self.__get_related_class()
        objects_to_update = await obj.get_uninvested_objects(self.session)
        for object in objects_to_update:
            amount_to_spend = object.full_amount - object.invested_amount
            if self.object.full_amount > amount_to_spend:
                self.object.invested_amount += amount_to_spend
                self.__close_object(object)
                self.session.add(object)
            else:
                object.invested_amount += self.object.full_amount
                if object.full_amount == object.invested_amount:
                    self.__close_object(object)
                    self.session.add(object)
                self.__close_object(self.object)
                self.session.add(self.object)
                break

        await self.session.commit()
        await self.session.refresh(self.object)
        return self.object
