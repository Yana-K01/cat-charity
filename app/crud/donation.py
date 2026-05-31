from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.schemas.donation import DonationCreate


async def get_multi(session: AsyncSession) -> list[Donation]:
    db_result = await session.execute(select(Donation).order_by(Donation.id))
    return list(db_result.scalars().all())


async def create(
    obj_in: DonationCreate,
    session: AsyncSession,
    *,
    commit: bool = True,
    user_id: int,
) -> Donation:
    data = obj_in.model_dump()
    data['comment'] = data.get('comment') or ''
    donation = Donation(**data, user_id=user_id)
    session.add(donation)

    if commit:
        await session.commit()
        await session.refresh(donation)
    else:
        await session.flush()

    return donation


# Метод для получения донатов пользователя
async def get_by_user(
    session: AsyncSession,
    user_id: int,
) -> list[Donation]:
    result = await session.execute(
        select(Donation).where(Donation.user_id == user_id)
    )

    return result.scalars().all()
