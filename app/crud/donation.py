from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class DonationCRUD(CRUDBase):
    """
    CRUD для модели пожертвования.
    """

    async def get_user_donations(
            self,
            user: User,
            session: AsyncSession
    ) -> list[Donation]:
        db_objs = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_objs.scalars().all()


donation_crud = DonationCRUD(Donation)
