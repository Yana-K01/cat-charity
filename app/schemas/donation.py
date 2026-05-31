from __future__ import annotations

from datetime import datetime

from pydantic import PositiveInt, BaseModel, ConfigDict


class DonationBase(BaseModel):
    comment: str = ''
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    full_amount: PositiveInt
    comment: str | None = None
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None = None
