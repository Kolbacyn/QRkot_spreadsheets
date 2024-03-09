from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import AbstractModel


class Donation(AbstractModel):
    """Модель пожертвования."""
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
