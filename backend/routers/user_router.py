from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user.create_branch_request import CreateBranchRequest
from schemas.user.update_branch_request import UpdateBranchRequest
from schemas.user.create_unit_request import CreateUnitRequest

from di.user_providers import get_create_branch_uc, get_update_branch_uc, get_create_unit_uc
from app.data.db import get_session
from app.security.dependencies import get_current_user

router = APIRouter()


@router.post("/branch")
async def create_branch(
    payload: CreateBranchRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    create_branch_uc = get_create_branch_uc(session)
    await create_branch_uc.execute(payload.name, _user.permissions)

    return {"success": True}


@router.patch("/branch/{branch_id}")
async def update_branch(
    branch_id: str,
    payload: UpdateBranchRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    update_branch_uc = get_update_branch_uc(session)
    await update_branch_uc.execute(branch_id, payload.name, _user.permissions)

    return {"success": True}


@router.post("/unit")
async def create_unit(
    payload: CreateUnitRequest,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    create_unit_uc = get_create_unit_uc(session)
    await create_unit_uc.execute(payload.name, payload.branch_id, current_user.permissions)

    return {"success": True}