from datetime import date

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db import get_session
from app.rate_limit.rate_limit_dependency import rate_limit
from app.security.cron_api_key_dependency import verify_cron_api_key
from app.security.dependencies import get_current_user

from schemas.meals.bulk_reserve_request import BulkReserveRequest
from schemas.meals.count_response import CountResponse
from schemas.meals.create_meal_plan_request import CreateMealPlanRequest
from schemas.meals.day_reservation_report_response import (
    DayReservationReportByBranchResponse,
    DayReservationReportResponse,
)
from schemas.meals.meal_plan_response import MealPlanResponse
from schemas.meals.meal_response import MealResponse
from schemas.meals.recurring_response import RecurringItemResponse
from schemas.meals.redeem_meal_request import RedeemMealRequest
from schemas.meals.reserve_meal_request import ReserveMealRequest
from schemas.meals.set_active_status_request import SetActiveStatusRequest
from schemas.meals.set_guest_count_request import SetGuestCountRequest
from schemas.meals.set_recurring_request import SetRecurringRequest
from schemas.meals.set_time_policies_request import SetTimePoliciesRequest
from schemas.meals.time_policy_response import TimePolicyResponse
from schemas.meals.update_meal_plan_request import UpdateMealPlanRequest
from schemas.meals.average_response import AverageResponse
from schemas.meals.meal_trend_response import MealTrendItem
from schemas.meals.branch_usage_response import BranchUsageItem

from di.meals_providers import (
    get_active_meals_count_uc,
    get_active_users_count_uc,
    get_branches_count_uc,
    get_bulk_reserve_meal_uc,
    get_cancel_reservation_uc,
    get_create_meal_plan_uc,
    get_create_meal_uc,
    get_day_reservation_report_by_branch_uc,
    get_day_reservation_report_uc,
    get_delete_meal_plan_uc,
    get_meal_photo_uc,
    get_meal_plan_recurring_uc,
    get_meal_plan_time_policies_uc,
    get_meal_plans_uc,
    get_meals_uc,
    get_redeem_meal_uc,
    get_reserve_meal_uc,
    get_run_meal_plan_recurring_cron_uc,
    get_set_guest_count_uc,
    get_set_meal_active_status_uc,
    get_set_meal_plan_recurring_uc,
    get_set_meal_plan_time_policies_uc,
    get_update_meal_plan_uc,
    get_update_meal_uc,
    get_average_guests_uc,
    get_meal_trend_uc,
    get_branch_usage_uc,
)


router = APIRouter()


@router.put("/meal-plan-time-policies")
async def set_meal_plan_time_policies(
    payload: SetTimePoliciesRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    set_policies_uc = await get_set_meal_plan_time_policies_uc(session)
    policies = [{"target_weekday": p.target_weekday, "cutoff_before": p.cutoff_before} for p in payload.policies]

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
        TimePolicyResponse(id=p.id, target_weekday=p.target_weekday.value, cutoff_before=p.cutoff_before)
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
    plans = await get_plans_uc.execute(date_from, date_to, _user.id)

    return [
        MealPlanResponse(
            id=p.id,
            plan_date=p.plan_date,
            meal=MealResponse(**vars(p.meal)),
            is_reserved=p.is_reserved,
        )
        for p in plans
    ]


@router.put("/meal-plan-recurring")
async def set_meal_plan_recurring(
    payload: SetRecurringRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = await get_set_meal_plan_recurring_uc(session)
    items = [{"target_date": i.target_date, "meal_id": i.meal_id} for i in payload.items]

    await uc.execute(items, _user.permissions)

    return {"success": True}


@router.get("/meal-plan-recurring", response_model=list[RecurringItemResponse])
async def get_meal_plan_recurring(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_meal_plan_recurring_uc(session)
    items = await uc.execute(_user.permissions)

    return [RecurringItemResponse(target_date=i.target_date, meal_id=i.meal_id) for i in items]


@router.post("/cron/meal-plan-recurring")
async def run_meal_plan_recurring_cron(
    session: AsyncSession = Depends(get_session),
    _api_key=Depends(verify_cron_api_key),
):
    uc = await get_run_meal_plan_recurring_cron_uc(session)
    await uc.execute()

    return {"success": True}


@router.post("/voucher")
async def reserve_meal(
    payload: ReserveMealRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
    _rate_limit=Depends(rate_limit(scope="reserve_meal", max_requests=10, window_seconds=60)),
):
    reserve_meal_uc = await get_reserve_meal_uc(session)
    await reserve_meal_uc.execute(_user.id, payload.meal_plan_id)

    return {"success": True}


@router.delete("/voucher/{meal_plan_id}")
async def cancel_reservation(
    meal_plan_id: str,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
    _rate_limit=Depends(rate_limit(scope="cancel_reservation", max_requests=10, window_seconds=60)),
):
    cancel_reservation_uc = await get_cancel_reservation_uc(session)
    await cancel_reservation_uc.execute(_user.id, meal_plan_id)

    return {"success": True}


@router.post("/voucher/bulk")
async def bulk_reserve_meal(
    payload: BulkReserveRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
    _rate_limit=Depends(rate_limit(scope="bulk_reserve_meal", max_requests=10, window_seconds=60)),
):
    uc = await get_bulk_reserve_meal_uc(session)
    items = [{"user_id": i.user_id, "reserve": i.reserve} for i in payload.items]

    return await uc.execute(payload.meal_plan_id, items, _user.permissions)


@router.post("/voucher/redeem")
async def redeem_meal(
    payload: RedeemMealRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_redeem_meal_uc(session)
    return await uc.execute(payload.rfid_card_id, _user.permissions)


@router.get("/voucher/day", response_model=DayReservationReportResponse)
async def get_day_reservation_report(
    plan_date: date,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_day_reservation_report_uc(session)
    return await uc.execute(plan_date, _user.permissions, _user.id)


@router.get("/voucher/day/all", response_model=DayReservationReportByBranchResponse)
async def get_day_reservation_report_by_branch(
    plan_date: date,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_day_reservation_report_by_branch_uc(session)
    return await uc.execute(plan_date, _user.permissions)


@router.put("/guest")
async def set_guest_count(
    payload: SetGuestCountRequest,
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = await get_set_guest_count_uc(session)
    guest_count = await uc.execute(
        payload.meal_plan_id, payload.unit_id, payload.guest_count, _user.id, _user.permissions
    )

    return {"success": True, "guest_count": guest_count}


@router.get("/reports/users-count", response_model=CountResponse)
async def get_active_users_count(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_active_users_count_uc(session)
    return CountResponse(count=await uc.execute(_user.permissions))


@router.get("/reports/meals-count", response_model=CountResponse)
async def get_active_meals_count(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_active_meals_count_uc(session)
    return CountResponse(count=await uc.execute(_user.permissions))


@router.get("/reports/branches-count", response_model=CountResponse)
async def get_branches_count(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_branches_count_uc(session)
    return CountResponse(count=await uc.execute(_user.permissions))




@router.get("/reports/average-guests", response_model=AverageResponse)
async def get_average_guests(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_average_guests_uc(session)
    return AverageResponse(average=await uc.execute(_user.permissions))



@router.get("/reports/meal-trend", response_model=list[MealTrendItem])
async def get_meal_trend(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_meal_trend_uc(session)
    return await uc.execute(_user.permissions)



@router.get("/reports/branch-usage", response_model=list[BranchUsageItem])
async def get_branch_usage(
    session: AsyncSession = Depends(get_session),
    _user=Depends(get_current_user),
):
    uc = get_branch_usage_uc(session)
    return await uc.execute(_user.permissions)