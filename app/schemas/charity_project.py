from __future__ import annotations

from typing import Annotated

from pydantic import Field, PositiveInt

from app.schemas.base import BaseSchema, InvestmentBaseDB


NameStr = Annotated[str, Field(min_length=5, max_length=100)]
DescStr = Annotated[str, Field(min_length=10)]


class CharityProjectCreate(BaseSchema):
    name: NameStr
    description: DescStr
    full_amount: PositiveInt


class CharityProjectUpdate(BaseSchema):
    name: NameStr | None = None
    description: DescStr | None = None
    full_amount: PositiveInt | None = None


class CharityProjectDB(InvestmentBaseDB):
    id: int
    name: NameStr
    description: DescStr
