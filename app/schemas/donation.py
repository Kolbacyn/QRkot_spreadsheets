from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt

from app.services import constants as const


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        example=1451
    )
    comment: Optional[str] = Field(
        None,
        example=const.EXAMPLE
    )


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationCreate):
    id: PositiveInt
    create_date: datetime
    invested_amount: NonNegativeInt
    fully_invested: Optional[bool]
    close_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True
