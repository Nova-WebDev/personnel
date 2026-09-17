from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.meals.set_time_policies_request import SetTimePoliciesRequest
from schemas.meals.time_policy_response import TimePolicyResponse

from di.meals_providers import get_set_meal_plan_time_policies_uc, get_meal_plan_time_policies_uc, get_create_meal_uc, get_update_meal_uc
from app.data.db import get_session
from app.security.dependencies import get_current_user

router = APIRouter()


@router.put("/meal-plan-time-policies")
async def set_meal_plan_time_policies(
    payload: SetTimePoliciesRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    set_policies_uc = await get_set_meal_plan_time_policies_uc(session)
    policies = [{"target_weekday": p.target_weekday, "cutoff_hours_before": p.cutoff_hours_before} for p in payload.policies]

    await set_policies_uc.execute(policies, _user.permissions)

    return {"success": True}


@router.get("/meal-plan-time-policies", response_model=list[TimePolicyResponse])
async def get_meal_plan_time_policies(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    get_policies_uc = await get_meal_plan_time_policies_uc(session)
    policies = await get_policies_uc.execute()

    return [
        TimePolicyResponse(id=p.id, target_weekday=p.target_weekday.value, cutoff_hours_before=p.cutoff_hours_before)
        for p in policies
    ]



@router.post("/meal")
async def create_meal(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
    title: str = Form(...),
    description: str | None = Form(None),
    photo: UploadFile | None = File(None),
):
    create_meal_uc = await get_create_meal_uc(session)
    file_bytes = await photo.read() if photo is not None else None

    await create_meal_uc.execute(
        title=title,
        permissions=_user.permissions,
        description=description,
        file_bytes=file_bytes,
    )

    return {"success": True}




@router.patch("/meal/{meal_id}")
async def update_meal(
    meal_id: str,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
    title: str = Form(...),
    description: str | None = Form(None),
    photo: UploadFile | None = File(None),
):
    update_meal_uc = await get_update_meal_uc(session)
    file_bytes = await photo.read() if photo is not None else None

    await update_meal_uc.execute(
        meal_id=meal_id,
        title=title,
        permissions=_user.permissions,
        description=description,
        file_bytes=file_bytes,
    )

    return {"success": True}