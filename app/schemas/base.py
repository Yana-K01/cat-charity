from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')


class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class InvestmentBaseDB(ORMBaseSchema):
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None
