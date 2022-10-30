from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer


class BaseModel:

    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount >= 0'),
        CheckConstraint('full_amount >= invested_amount')
    )

    def __repr__(self):
        return (
            f'Полная сумма: {self.full_amount}, Проинвестированная сумма: {self.invested_amount},'
            f'Все проинвестированно: {self.fully_invested}, Дата создания: {self.create_date},'
            f'Дата закрытия:{self.close_date}'
        )
