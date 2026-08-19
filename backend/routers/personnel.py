import uuid

from fastapi import APIRouter, Depends, Form, UploadFile, File, Response

from sqlalchemy.ext.asyncio import AsyncSession

from personnel.core.entities.position import PersonnelPosition

from personnel.infrastructure.security.rate_limit_dependency import rate_limit
from personnel.infrastructure.security.api_key_dependency import verify_api_key

from schemas.personnel.create_branch_request import CreateBranchRequest
from schemas.personnel.branch_response import BranchResponse
from schemas.personnel.create_unit_request import CreateUnitRequest
from schemas.personnel.unit_response import UnitResponse
from schemas.personnel.update_branch_request import UpdateBranchRequest
from schemas.personnel.update_unit_name_request import UpdateUnitNameRequest
from schemas.personnel.branch_with_units_response import BranchWithUnitsResponse
from schemas.personnel.unit_nested_response import UnitNestedResponse
from schemas.personnel.personnel_response import PersonnelResponse
from schemas.personnel.set_block_status_request import SetBlockStatusRequest
from schemas.personnel.get_personnel_query import GetPersonnelQuery
from schemas.personnel.personnel_paginated_response import PersonnelPaginatedResponse
from schemas.personnel.personnel_detail_response import PersonnelDetailResponse

from di.personnel_providers import (
    get_create_branch_uc,
    get_create_unit_uc,
    get_update_branch_uc,
    get_delete_branch_uc,
    get_update_unit_name_uc,
    get_delete_unit_uc,
    get_all_branches_with_units_uc,
    get_create_personnel_uc,
    get_update_personnel_uc,
    get_set_personnel_block_status_uc,
    get_personnel_paginated_uc,
    get_personnel_photo_uc,
    get_personnel_qr_code_uc,
    get_personnel_detail_uc,
)
from app.data.db import get_session
from app.security.dependencies import get_current_user


router = APIRouter(prefix="/personnel", tags=["personnel"])


@router.post("/branches", response_model=BranchResponse)
async def create_branch(
    payload: CreateBranchRequest,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    create_branch_uc = get_create_branch_uc(session)
    branch_entity = await create_branch_uc.execute(payload.name)

    return BranchResponse(
        id=branch_entity.id,
        name=branch_entity.name,
    )


@router.post("/units", response_model=UnitResponse)
async def create_unit(
    payload: CreateUnitRequest,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    create_unit_uc = get_create_unit_uc(session)
    unit_entity = await create_unit_uc.execute(payload.name, payload.branch_id)

    return UnitResponse(
        id=unit_entity.id,
        name=unit_entity.name,
        branch_id=unit_entity.branch_id,
    )


@router.put("/branches/{branch_id}", response_model=BranchResponse)
async def update_branch(
    branch_id: int,
    payload: UpdateBranchRequest,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    update_branch_uc = get_update_branch_uc(session)
    branch_entity = await update_branch_uc.execute(branch_id, payload.name)

    return BranchResponse(
        id=branch_entity.id,
        name=branch_entity.name,
    )


@router.delete("/branches/{branch_id}")
async def delete_branch(
    branch_id: int,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    delete_branch_uc = get_delete_branch_uc(session)
    await delete_branch_uc.execute(branch_id)

    return {"success": True}


@router.put("/units/{unit_id}")
async def update_unit_name(
    unit_id: int,
    payload: UpdateUnitNameRequest,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    update_unit_name_uc = get_update_unit_name_uc(session)
    await update_unit_name_uc.execute(unit_id, payload.name)

    return {"success": True}


@router.delete("/units/{unit_id}")
async def delete_unit(
    unit_id: int,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    delete_unit_uc = get_delete_unit_uc(session)
    await delete_unit_uc.execute(unit_id)

    return {"success": True}


@router.get("/branches", response_model=list[BranchWithUnitsResponse])
async def get_all_branches(
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    get_all_branches_uc = get_all_branches_with_units_uc(session)
    branches = await get_all_branches_uc.execute()

    return [
        BranchWithUnitsResponse(
            id=branch.id,
            name=branch.name,
            units=[
                UnitNestedResponse(id=unit.id, name=unit.name)
                for unit in branch.units
            ],
        )
        for branch in branches
    ]




@router.post("/", response_model=PersonnelResponse)
async def create_personnel(
    personnel_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    branch_id: int = Form(...),
    unit_id: int | None = Form(None),
    position: PersonnelPosition | None = Form(None),
    file: UploadFile | None = File(None),
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    create_personnel_uc = get_create_personnel_uc(session)
    file_bytes = await file.read() if file else None

    personnel_entity = await create_personnel_uc.execute(
        personnel_id=personnel_id,
        first_name=first_name,
        last_name=last_name,
        branch_id=branch_id,
        unit_id=unit_id,
        file_bytes=file_bytes,
        position=position,
    )

    return PersonnelResponse(
        uuid=personnel_entity.uuid,
        personnel_id=personnel_entity.personnel_id,
        first_name=personnel_entity.first_name,
        last_name=personnel_entity.last_name,
        branch_id=personnel_entity.branch_id,
        unit_id=personnel_entity.unit_id,
        photo_path=personnel_entity.photo_path,
        position=personnel_entity.position,
        is_blocked=personnel_entity.is_blocked,
    )


@router.put("/{personnel_uuid}", response_model=PersonnelResponse)
async def update_personnel(
    personnel_uuid: uuid.UUID,
    personnel_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    branch_id: int = Form(...),
    unit_id: int | None = Form(None),
    position: PersonnelPosition | None = Form(None),
    file: UploadFile | None = File(None),
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    update_personnel_uc = get_update_personnel_uc(session)
    file_bytes = await file.read() if file else None

    personnel_entity = await update_personnel_uc.execute(
        personnel_uuid=personnel_uuid,
        personnel_id=personnel_id,
        first_name=first_name,
        last_name=last_name,
        branch_id=branch_id,
        unit_id=unit_id,
        position=position,
        file_bytes=file_bytes,
    )

    return PersonnelResponse(
        uuid=personnel_entity.uuid,
        personnel_id=personnel_entity.personnel_id,
        first_name=personnel_entity.first_name,
        last_name=personnel_entity.last_name,
        branch_id=personnel_entity.branch_id,
        unit_id=personnel_entity.unit_id,
        photo_path=personnel_entity.photo_path,
        position=personnel_entity.position,
        is_blocked=personnel_entity.is_blocked,
    )

@router.patch("/{personnel_uuid}/block-status")
async def set_personnel_block_status(
    personnel_uuid: uuid.UUID,
    payload: SetBlockStatusRequest,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    set_block_status_uc = get_set_personnel_block_status_uc(session)
    await set_block_status_uc.execute(personnel_uuid, payload.is_blocked)

    return {"success": True}


@router.get("/", response_model=PersonnelPaginatedResponse)
async def get_personnel_paginated(
    query: GetPersonnelQuery = Depends(),
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    get_personnel_uc = get_personnel_paginated_uc(session)
    result = await get_personnel_uc.execute(
        page=query.page,
        limit=query.limit,
        search=query.search,
        order_by=query.order_by,
        descending=query.descending,
    )

    return PersonnelPaginatedResponse(
        personnel=[
            PersonnelResponse(
                uuid=p.uuid,
                personnel_id=p.personnel_id,
                first_name=p.first_name,
                last_name=p.last_name,
                branch_id=p.branch_id,
                unit_id=p.unit_id,
                photo_path=p.photo_path,
                position=p.position,
                is_blocked=p.is_blocked,
            )
            for p in result["personnel"]
        ],
        total_count=result["total_count"],
    )




@router.get("/photo/{file_id}")
async def get_personnel_photo(
    file_id: str,
    _rate_limit=Depends(rate_limit(scope="photo", max_requests=30, window_seconds=60)),
):
    get_photo_uc = get_personnel_photo_uc()
    data = await get_photo_uc.execute(file_id)
    return Response(content=data, media_type="image/png")

@router.get("/{personnel_uuid}/qr")
async def get_personnel_qr_code(
    personnel_uuid: uuid.UUID,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    get_qr_uc = get_personnel_qr_code_uc(session)
    qr_bytes = await get_qr_uc.execute(personnel_uuid)
    return Response(content=qr_bytes, media_type="image/png")




@router.get("/{personnel_uuid}", response_model=PersonnelDetailResponse)
async def get_personnel_detail_public(
    personnel_uuid: uuid.UUID,
    _rate_limit=Depends(rate_limit(scope="detail", max_requests=30, window_seconds=60)),
    session: AsyncSession = Depends(get_session),
):
    get_detail_uc = get_personnel_detail_uc(session)
    personnel = await get_detail_uc.execute(personnel_uuid)

    return PersonnelDetailResponse(
        uuid=personnel.uuid,
        personnel_id=personnel.personnel_id,
        first_name=personnel.first_name,
        last_name=personnel.last_name,
        photo_path=personnel.photo_path,
        position=personnel.position,
        is_blocked=personnel.is_blocked,
        branch_name=personnel.branch_name,
        unit_name=personnel.unit_name,
    )


@router.get("/verify/{personnel_uuid}", response_model=PersonnelDetailResponse)
async def get_personnel_detail_verified(
    personnel_uuid: uuid.UUID,
    _api_key=Depends(verify_api_key),
    session: AsyncSession = Depends(get_session),
):
    get_detail_uc = get_personnel_detail_uc(session)
    personnel = await get_detail_uc.execute(personnel_uuid)

    return PersonnelDetailResponse(
        uuid=personnel.uuid,
        personnel_id=personnel.personnel_id,
        first_name=personnel.first_name,
        last_name=personnel.last_name,
        photo_path=personnel.photo_path,
        position=personnel.position,
        is_blocked=personnel.is_blocked,
        branch_name=personnel.branch_name,
        unit_name=personnel.unit_name,
    )