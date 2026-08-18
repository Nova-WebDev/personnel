import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.personnel.create_branch_request import CreateBranchRequest
from schemas.personnel.branch_response import BranchResponse
from schemas.personnel.create_unit_request import CreateUnitRequest
from schemas.personnel.unit_response import UnitResponse
from schemas.personnel.update_branch_request import UpdateBranchRequest
from schemas.personnel.update_unit_name_request import UpdateUnitNameRequest
from schemas.personnel.branch_with_units_response import BranchWithUnitsResponse
from schemas.personnel.unit_nested_response import UnitNestedResponse
from schemas.personnel.create_personnel_request import CreatePersonnelRequest
from schemas.personnel.personnel_response import PersonnelResponse
from schemas.personnel.update_personnel_request import UpdatePersonnelRequest
from schemas.personnel.set_block_status_request import SetBlockStatusRequest

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
    payload: CreatePersonnelRequest,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    create_personnel_uc = get_create_personnel_uc(session)
    personnel_entity = await create_personnel_uc.execute(
        personnel_id=payload.personnel_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        branch_id=payload.branch_id,
        unit_id=payload.unit_id,
        position=payload.position,
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
    payload: UpdatePersonnelRequest,
    _user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    update_personnel_uc = get_update_personnel_uc(session)
    personnel_entity = await update_personnel_uc.execute(
        personnel_uuid=personnel_uuid,
        personnel_id=payload.personnel_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        branch_id=payload.branch_id,
        unit_id=payload.unit_id,
        position=payload.position,
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