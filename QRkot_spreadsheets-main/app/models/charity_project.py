from sqlalchemy import Column, String, Text

from app.core.db import Base

from .base_model import BaseModelMixin


class CharityProject(Base, BaseModelMixin):
    __tablename__ = 'charityproject'

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
