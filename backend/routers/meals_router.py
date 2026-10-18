from datetime import date
from fastapi import APIRouter, Depends, Form, UploadFile, File, Response
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.meals.set_time_policies_request import SetTimePoliciesRequest
from schemas.meals.time_policy_response import TimePolicyResponse
from schemas.meals.set_active_status_request import SetActiveStatusRequest
from schemas.meals.create_meal_plan_request import CreateMealPlanRequest
from schemas.meals.update_meal_plan_request import UpdateMealPlanRequest
from schemas.meals.meal_plan_response import MealPlanResponse
from schemas.meals.meal_response import MealResponse

from di.meals_providers import get_set_meal_plan_time_policies_uc, get_meal_plan_time_policies_uc, get_create_meal_uc, get_update_meal_uc, get_set_meal_active_status_uc, get_meals_uc, get_create_meal_plan_uc, get_update_meal_plan_uc, get_delete_meal_plan_uc, get_meal_plans_uc, get_meal_photo_uc
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




@router.patch("/meal/{meal_id}/active-status")
async def set_meal_active_status(
    meal_id: str,
    payload: SetActiveStatusRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    set_status_uc = await get_set_meal_active_status_uc(session)
    await set_status_uc.execute(meal_id, payload.is_active, _user.permissions)

    return {"success": True}



@router.get("/meal", response_model=list[MealResponse])
async def get_meals(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    get_meals_uc_instance = await get_meals_uc(session)
    meals = await get_meals_uc_instance.execute(_user.permissions)

    return [MealResponse(**vars(m)) for m in meals]



@router.post("/meal-plan")
async def create_meal_plan(
    payload: CreateMealPlanRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    create_meal_plan_uc = await get_create_meal_plan_uc(session)
    await create_meal_plan_uc.execute(payload.plan_date, payload.meal_id, _user.permissions)

    return {"success": True}




@router.patch("/meal-plan/{meal_plan_id}")
async def update_meal_plan(
    meal_plan_id: str,
    payload: UpdateMealPlanRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    update_meal_plan_uc = await get_update_meal_plan_uc(session)
    await update_meal_plan_uc.execute(meal_plan_id, payload.meal_id, _user.permissions)

    return {"success": True}


@router.delete("/meal-plan/{meal_plan_id}")
async def delete_meal_plan(
    meal_plan_id: str,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    delete_meal_plan_uc = await get_delete_meal_plan_uc(session)
    await delete_meal_plan_uc.execute(meal_plan_id, _user.permissions)

    return {"success": True}


@router.get("/meal-plan", response_model=list[MealPlanResponse])
async def get_meal_plans(
    date_from: date,
    date_to: date,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    get_plans_uc = get_meal_plans_uc(session)
    plans = await get_plans_uc.execute(date_from, date_to)

    return [
        MealPlanResponse(
            id=p.id,
            plan_date=p.plan_date,
            meal=MealResponse(**vars(p.meal)),
        )
        for p in plans
    ]


@router.get("/meal/{meal_id}/photo")
async def get_meal_photo(
    meal_id: str,
    _user=Depends(get_current_user),
):
    photo_bytes = await get_meal_photo_uc().execute(meal_id)

    return Response(
        content=photo_bytes,
        media_type="image/png",
        headers={"Cache-Control": "no-cache"},
    )