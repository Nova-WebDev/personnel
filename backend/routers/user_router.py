from fastapi import APIRouter, Depends, Form, UploadFile, File, Response
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user.create_branch_request import CreateBranchRequest
from schemas.user.update_branch_request import UpdateBranchRequest
from schemas.user.create_unit_request import CreateUnitRequest
from schemas.user.update_unit_request import UpdateUnitRequest
from schemas.user.branch_with_units_response import BranchWithUnitsResponse, UnitResponse
from schemas.user.user_with_location_response import UserWithLocationResponse
from schemas.user.set_blocked_status_request import SetBlockedStatusRequest
from schemas.user.user_profile_response import UserProfileResponse, ScopeInfoResponse

from di.user_providers import get_create_branch_uc, get_update_branch_uc, get_create_unit_uc, get_update_unit_uc, get_delete_branch_uc, get_delete_unit_uc, get_branches_with_units_uc, get_users_with_location_uc, get_create_user_uc, get_update_user_uc, get_set_user_blocked_status_uc, get_user_qr_code_uc, get_profile_photo_uc, get_my_profile_uc
from app.data.db import get_session
from app.security.dependencies import get_current_user
from app.security.rate_limit_dependency import rate_limit

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
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
    phone: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    unit_id: str = Form(...),
    personnel_code: str | None = Form(None),
    photo: UploadFile | None = File(None),
):
    create_user_uc = get_create_user_uc(session)

    file_bytes = await photo.read() if photo is not None else None

    await create_user_uc.execute(
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        unit_id=unit_id,
        permissions=_user.permissions,
        personnel_code=personnel_code,
        file_bytes=file_bytes,
    )

    return {"success": True}


@router.patch("/user/{user_id}")
async def update_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
    phone: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    unit_id: str = Form(...),
    personnel_code: str | None = Form(None),
    photo: UploadFile | None = File(None),
):
    update_user_uc = get_update_user_uc(session)

    file_bytes = await photo.read() if photo is not None else None

    await update_user_uc.execute(
        user_id=user_id,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        unit_id=unit_id,
        permissions=_user.permissions,
        personnel_code=personnel_code,
        file_bytes=file_bytes,
    )

    return {"success": True}


@router.get("/photo/{file_id}")
async def get_profile_photo(
    file_id: str,
    _rate_limit=Depends(rate_limit(scope="profile_photo", max_requests=30, window_seconds=60)),
):
    get_photo_uc = get_profile_photo_uc()
    data = await get_photo_uc.execute(file_id)
    return Response(content=data, media_type="image/png")

@router.patch("/user/{user_id}/blocked-status")
async def set_user_blocked_status(
    user_id: str,
    payload: SetBlockedStatusRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    set_blocked_status_uc = get_set_user_blocked_status_uc(session)
    await set_blocked_status_uc.execute(user_id, payload.is_blocked, _user.permissions)

    return {"success": True}



@router.get("/user/{user_id}/qrcode")
async def get_user_qr_code(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    get_qr_uc = get_user_qr_code_uc(session)
    qr_bytes = await get_qr_uc.execute(user_id, _user.permissions)

    return Response(content=qr_bytes, media_type="image/png")

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    get_profile_uc = get_my_profile_uc(session)
    profile = await get_profile_uc.execute(_user.id, _user.permissions)

    return UserProfileResponse(
        id=profile.id,
        phone=profile.phone,
        first_name=profile.first_name,
        last_name=profile.last_name,
        personnel_code=profile.personnel_code,
        rfid_card_id=profile.rfid_card_id,
        photo_path=profile.photo_path,
        is_blocked=profile.is_blocked,
        created_at=profile.created_at,
        unit_id=profile.unit_id,
        unit_name=profile.unit_name,
        branch_id=profile.branch_id,
        branch_name=profile.branch_name,
        scopes=[
            ScopeInfoResponse(
                level=s.level,
                unit_id=s.unit_id,
                unit_name=s.unit_name,
                branch_id=s.branch_id,
                branch_name=s.branch_name,
            )
            for s in profile.scopes
        ],
    )