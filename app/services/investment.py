from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def _close_if_fully_invested(investment_target: CharityProject | Donation,
                             now: datetime) -> None:
    if (investment_target.invested_amount >= investment_target.full_amount and
       not investment_target.fully_invested):
        investment_target.invested_amount = investment_target.full_amount
        investment_target.fully_invested = True
        investment_target.close_date = now


async def _get_open_projects(session: AsyncSession) -> list[CharityProject]:
    result = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(CharityProject.create_date, CharityProject.id)
    )
    return list(result.scalars().all())


async def _get_open_donations(session: AsyncSession) -> list[Donation]:
    result = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date, Donation.id)
    )
    return list(result.scalars().all())


async def invest_donation(
    donation: Donation,
    session: AsyncSession,
    *,
    now: datetime | None = None,
) -> None:
    if donation.fully_invested:
        return

    now = now or datetime.utcnow()
    projects = await _get_open_projects(session)

    for project in projects:
        if donation.fully_invested:
            break
        if project.fully_invested:
            continue

        donation_left = donation.full_amount - donation.invested_amount
        project_left = project.full_amount - project.invested_amount

        if donation_left <= 0:
            _close_if_fully_invested(donation, now)
            break
        if project_left <= 0:
            _close_if_fully_invested(project, now)
            continue

        to_invest = min(donation_left, project_left)

        donation.invested_amount += to_invest
        project.invested_amount += to_invest

        _close_if_fully_invested(project, now)
        _close_if_fully_invested(donation, now)

    await session.flush()


async def invest_project(
    project: CharityProject,
    session: AsyncSession,
    *,
    now: datetime | None = None,
) -> None:
    if project.fully_invested:
        return

    now = now or datetime.utcnow()
    donations = await _get_open_donations(session)

    for donation in donations:
        if project.fully_invested:
            break
        if donation.fully_invested:
            continue

        project_left = project.full_amount - project.invested_amount
        donation_left = donation.full_amount - donation.invested_amount

        if project_left <= 0:
            _close_if_fully_invested(project, now)
            break
        if donation_left <= 0:
            _close_if_fully_invested(donation, now)
            continue

        to_invest = min(project_left, donation_left)

        project.invested_amount += to_invest
        donation.invested_amount += to_invest

        _close_if_fully_invested(donation, now)
        _close_if_fully_invested(project, now)

    await session.flush()
