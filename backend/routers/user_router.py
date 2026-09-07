from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user.create_branch_request import CreateBranchRequest
from schemas.user.update_branch_request import UpdateBranchRequest
from schemas.user.create_unit_request import CreateUnitRequest
from schemas.user.update_unit_request import UpdateUnitRequest
from schemas.user.branch_with_units_response import BranchWithUnitsResponse, UnitResponse
from schemas.user.user_with_location_response import UserWithLocationResponse
from schemas.user.create_user_request import CreateUserRequest

from di.user_providers import get_create_branch_uc, get_update_branch_uc, get_create_unit_uc, get_update_unit_uc, get_delete_branch_uc, get_delete_unit_uc, get_branches_with_units_uc, get_users_with_location_uc, get_create_user_uc
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
    _user=Depends(get_current_user),
):
    create_unit_uc = get_create_unit_uc(session)
    await create_unit_uc.execute(payload.name, payload.branch_id, _user.permissions)

    return {"success": True}


@router.patch("/unit/{unit_id}")
async def update_unit(
    unit_id: str,
    payload: UpdateUnitRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    update_unit_uc = get_update_unit_uc(session)
    await update_unit_uc.execute(unit_id, payload.name, _user.permissions)

    return {"success": True}


@router.delete("/branch/{branch_id}")
async def delete_branch(
    branch_id: str,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    delete_branch_uc = get_delete_branch_uc(session)
    await delete_branch_uc.execute(branch_id, _user.permissions)

    return {"success": True}


@router.delete("/unit/{unit_id}")
async def delete_unit(
    unit_id: str,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    delete_unit_uc = get_delete_unit_uc(session)
    await delete_unit_uc.execute(unit_id, _user.permissions)

    return {"success": True}


@router.get("/branches", response_model=list[BranchWithUnitsResponse])
async def get_branches(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    get_branches_uc = get_branches_with_units_uc(session)
    branches = await get_branches_uc.execute(_user.permissions)

    return [
        BranchWithUnitsResponse(
            branch_id=b.branch_id,
            branch_name=b.branch_name,
            units=[UnitResponse(unit_id=u.id, unit_name=u.name) for u in b.units],
        )
        for b in branches
    ]

@router.get("/users", response_model=list[UserWithLocationResponse])
async def get_users(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    get_users_uc = get_users_with_location_uc(session)
    users = await get_users_uc.execute(_user.permissions)

    return [UserWithLocationResponse(**vars(u)) for u in users]

@router.post("/user")
async def create_user(
    payload: CreateUserRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    create_user_uc = get_create_user_uc(session)
    await create_user_uc.execute(
        phone=payload.phone,
        first_name=payload.first_name,
        last_name=payload.last_name,
        unit_id=payload.unit_id,
        permissions=_user.permissions,
        personnel_code=payload.personnel_code,
        photo_path=payload.photo_path,
    )

    return {"success": True}