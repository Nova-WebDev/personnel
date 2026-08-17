from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.personnel.create_branch_request import CreateBranchRequest
from schemas.personnel.branch_response import BranchResponse
from schemas.personnel.create_unit_request import CreateUnitRequest
from schemas.personnel.unit_response import UnitResponse
from schemas.personnel.update_branch_request import UpdateBranchRequest
from schemas.personnel.update_unit_name_request import UpdateUnitNameRequest

from di.personnel_providers import get_create_branch_uc, get_create_unit_uc, get_update_branch_uc, get_delete_branch_uc, get_update_unit_name_uc, get_delete_unit_uc
from app.data.db import get_session


router = APIRouter(prefix="/personnel", tags=["personnel"])


@router.post("/branches", response_model=BranchResponse)
async def create_branch(
    payload: CreateBranchRequest,
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
    session: AsyncSession = Depends(get_session),
):
    delete_branch_uc = get_delete_branch_uc(session)
    await delete_branch_uc.execute(branch_id)

    return {"success": True}


@router.put("/units/{unit_id}")
async def update_unit_name(
    unit_id: int,
    payload: UpdateUnitNameRequest,
    session: AsyncSession = Depends(get_session),
):
    update_unit_name_uc = get_update_unit_name_uc(session)
    await update_unit_name_uc.execute(unit_id, payload.name)

    return {"success": True}


@router.delete("/units/{unit_id}")
async def delete_unit(
    unit_id: int,
    session: AsyncSession = Depends(get_session),
):
    delete_unit_uc = get_delete_unit_uc(session)
    await delete_unit_uc.execute(unit_id)

    return {"success": True}