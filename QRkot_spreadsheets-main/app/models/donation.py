from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .base_model import BaseModelMixin


class Donation(Base, BaseModelMixin):
    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
