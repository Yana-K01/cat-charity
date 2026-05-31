from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import invest_donation

router = APIRouter(
    prefix='/donation',
    tags=list(('donations',)),
)


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    dependencies=(Depends(current_superuser),),
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> list[DonationFullInfoDB]:
    return await donation.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    status_code=200
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
) -> DonationDB:
    donation_object = await donation.create(donation_in,
                                            session,
                                            user_id=user.id,
                                            commit=False)
    await invest_donation(donation_object, session)
    await session.commit()
    await session.refresh(donation_object)
    return donation_object


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    return await donation.get_by_user(session, user.id)
