from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True