from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer


class BaseModelMixin:
    __table_args__ = (
        CheckConstraint(
            'full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            'invested_amount >= 0',
            name='check_invested_amount_non_negative'),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_not_exceeds_full'),
    )
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    full_amount = Column(Integer)
