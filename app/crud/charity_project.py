from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.investment import _close_if_fully_invested


async def get_multi(session: AsyncSession) -> list[CharityProject]:
    db_result = await session.execute(
        select(CharityProject).order_by(CharityProject.id)
    )
    return list(db_result.scalars().all())


async def get(project_id: int, session: AsyncSession) -> CharityProject:
    project = await session.get(CharityProject, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Charity project not found',
        )
    return project


async def _get_by_name(name: str,
                       session: AsyncSession) -> CharityProject | None:
    db_result = await session.execute(
        select(CharityProject).where(CharityProject.name == name)
    )
    return db_result.scalars().first()


async def _check_name_unique(
    name: str,
    session: AsyncSession,
    *,
    exclude_id: int | None = None,
) -> None:
    existing = await _get_by_name(name, session)
    if existing is None:
        return
    if exclude_id is not None and existing.id == exclude_id:
        return
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Проект с таким именем уже существует!',
    )


async def create(
    obj_in: CharityProjectCreate,
    session: AsyncSession,
    *,
    commit: bool = True,
) -> CharityProject:
    await _check_name_unique(obj_in.name, session)

    project = CharityProject(**obj_in.model_dump())
    session.add(project)

    if commit:
        await session.commit()
        await session.refresh(project)
    else:
        await session.flush()

    return project


async def update(
    project: CharityProject,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
    *,
    commit: bool = True,
) -> CharityProject:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )

    data = obj_in.model_dump(exclude_unset=True)
    data = {field: value for field, value in data.items() if value is not None}

    if 'name' in data:
        await _check_name_unique(data['name'], session, exclude_id=project.id)

    if 'full_amount' in data:
        new_full_amount = data['full_amount']
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=('Нелья установить значение full_amount меньше '
                        'уже вложенной суммы.'),
            )

    for field, value in data.items():
        setattr(project, field, value)

    _close_if_fully_invested(project, datetime.utcnow())

    if commit:
        await session.commit()
        await session.refresh(project)
    else:
        await session.flush()

    return project


async def remove(
    project: CharityProject,
    session: AsyncSession,
    *,
    commit: bool = True,
) -> CharityProject:
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )

    await session.delete(project)

    if commit:
        await session.commit()
    else:
        await session.flush()

    return project
