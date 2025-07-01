from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.database import get_async_session
from app.auth.fastapi_users import fastapi_users
from app.models.perfil import PerfilDeInteresse, PerfilDeInteresseCreate, PerfilDeInteresseUpdate, PerfilDeInteresseInDB
from app.models.user import User
from fastapi_users_db_sqlalchemy import UUID_ID

router = APIRouter()

current_active_user = fastapi_users.current_user(active=True)

@router.post(
    "/", response_model=PerfilDeInteresseInDB, status_code=status.HTTP_201_CREATED
)
async def create_perfil(
    perfil_in: PerfilDeInteresseCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    perfil = PerfilDeInteresse(**perfil_in.model_dump(), user_id=current_user.id)
    session.add(perfil)
    await session.commit()
    await session.refresh(perfil)
    return perfil

@router.get(
    "/", response_model=List[PerfilDeInteresseInDB]
)
async def read_perfis(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(PerfilDeInteresse).filter(PerfilDeInteresse.user_id == current_user.id)
    )
    perfis = result.scalars().all()
    return perfis

@router.get(
    "/{perfil_id}", response_model=PerfilDeInteresseInDB
)
async def read_perfil(
    perfil_id: UUID,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(PerfilDeInteresse).filter(
            PerfilDeInteresse.id == perfil_id,
            PerfilDeInteresse.user_id == current_user.id,
        )
    )
    perfil = result.scalars().first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil not found")
    return perfil

@router.put(
    "/{perfil_id}", response_model=PerfilDeInteresseInDB
)
async def update_perfil(
    perfil_id: UUID,
    perfil_in: PerfilDeInteresseUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(PerfilDeInteresse).filter(
            PerfilDeInteresse.id == perfil_id,
            PerfilDeInteresse.user_id == current_user.id,
        )
    )
    perfil = result.scalars().first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil not found")

    for field, value in perfil_in.model_dump(exclude_unset=True).items():
        setattr(perfil, field, value)

    session.add(perfil)
    await session.commit()
    await session.refresh(perfil)
    return perfil

@router.delete(
    "/{perfil_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_perfil(
    perfil_id: UUID,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(PerfilDeInteresse).filter(
            PerfilDeInteresse.id == perfil_id,
            PerfilDeInteresse.user_id == current_user.id,
        )
    )
    perfil = result.scalars().first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil not found")

    await session.delete(perfil)
    await session.commit()
    return