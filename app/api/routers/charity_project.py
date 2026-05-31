from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project as charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest_project

router = APIRouter(
    prefix='/charity_project',
    tags=list(('charity_projects',)),
)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[CharityProjectDB]:
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def create_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    superuser=Depends(current_superuser),
) -> CharityProjectDB:
    project = await charity_project_crud.create(project_in,
                                                session,
                                                commit=False)
    await invest_project(project, session)
    await session.commit()
    await session.refresh(project)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    superuser=Depends(current_superuser),
) -> CharityProjectDB:
    project = await charity_project_crud.get(project_id, session)
    project = await charity_project_crud.update(project,
                                                project_in,
                                                session,
                                                commit=False)
    await invest_project(project, session)
    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    superuser=Depends(current_superuser),
) -> CharityProjectDB:
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(status_code=400,
                            detail='Нельзя удалить проект с вложениями')
    await charity_project_crud.remove(project, session, commit=False)
    await session.commit()
    return project
