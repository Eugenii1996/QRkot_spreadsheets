from sqlalchemy import Column, String, Text

from app.core.db import Base
from .base import BaseModel


class CharityProject(BaseModel, Base):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{super().__repr__()}, Название проекта: {self.name},'
            f'Описание проекта: {self.description}'
        )
