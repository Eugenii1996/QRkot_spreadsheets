from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from .base import BaseModel


class Donation(BaseModel, Base):

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'{super().__repr__()}, ID пользователя: {self.user_id},'
            f'Комментарий: {self.comment}'
        )
