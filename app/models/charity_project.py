from sqlalchemy import Column, String, Text

from app.models.abstract import AbstractModel


class CharityProject(AbstractModel):
    """Модель благотворительного проекта."""
    name = Column(String)
    description = Column(Text)
