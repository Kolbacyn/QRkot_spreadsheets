from app.crud.donation import donation_crud
from app.models import Donation
from app.services.base_handler import BaseHandler


class DonationHandler(BaseHandler):
    """
    Класс для работы с пожертвованиями.
    """
    CRUD = donation_crud

    async def get_user_donations(self) -> list[Donation]:
        """
        Только для зарегистрированных пользователей.

        Возвращает список пожертвований пользователя.
        """
        user_donations = await donation_crud.get_user_donations(
            self.user, self.session
        )
        return user_donations
