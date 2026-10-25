from datetime import date

from pydantic import BaseModel

from schemas.meals.meal_response import MealResponse


class UnitInfoResponse(BaseModel):
    id: str
    name: str
    branch_id: str
    branch_name: str


class MemberInfoResponse(BaseModel):
    id: str
    phone: str
    first_name: str
    last_name: str
    personnel_code: str | None
    rfid_card_id: str | None
    photo_path: str | None
    is_blocked: bool
    is_reserved: bool
    meal_plan_id: str | None
    meal: MealResponse | None
    is_used: bool | None


class GuestSummaryResponse(BaseModel):
    meal_plan_id: str
    total: int
    mine: int | None


class UnitMembersResponse(BaseModel):
    unit: UnitInfoResponse
    members: list[MemberInfoResponse]
    guests: list[GuestSummaryResponse] = []


class DayMealPlanResponse(BaseModel):
    meal_plan_id: str
    meal: MealResponse


class DayReservationReportResponse(BaseModel):
    plan_date: date
    meal_plans: list[DayMealPlanResponse]
    units: list[UnitMembersResponse]


class BranchInfoResponse(BaseModel):
    id: str
    name: str


class BranchUnitsResponse(BaseModel):
    branch: BranchInfoResponse
    units: list[UnitMembersResponse]


class DayReservationReportByBranchResponse(BaseModel):
    plan_date: date
    meal_plans: list[DayMealPlanResponse]
    branches: list[BranchUnitsResponse]