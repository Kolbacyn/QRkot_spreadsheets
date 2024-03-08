from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        example='Save all the kitties!',
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        example='every dollar will help us save the kitties',
    )
    full_amount: Optional[PositiveInt] = Field(
        None,
        example=1451,
        description='The amount of funds needed to be collected'
    )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    description: str = Field(
        ...,
        min_length=1
    )
    full_amount: PositiveInt = Field(
        ...,
        example=1451
    )


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: PositiveInt
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
