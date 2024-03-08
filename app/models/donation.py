from sqlalchemy import Column, Integer, Text, ForeignKey

from app.models.abstract import AbstractModel


class Donation(AbstractModel):
    """Модель пожертвования."""
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
