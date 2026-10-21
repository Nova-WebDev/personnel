from dataclasses import dataclass, field
from datetime import date

from meals.core.entities.meal import Meal


@dataclass
class UnitInfo:
    id: str
    name: str
    branch_id: str
    branch_name: str


@dataclass
class MemberInfo:
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
    meal: Meal | None
    is_used: bool | None


@dataclass
class UnitMembers:
    unit: UnitInfo
    members: list[MemberInfo] = field(default_factory=list)


@dataclass
class DayMealPlan:
    meal_plan_id: str
    meal: Meal


@dataclass
class DayReservationReport:
    plan_date: date
    meal_plans: list[DayMealPlan]
    units: list[UnitMembers]

@dataclass
class BranchInfo:
    id: str
    name: str


@dataclass
class BranchUnits:
    branch: BranchInfo
    units: list[UnitMembers] = field(default_factory=list)


@dataclass
class DayReservationReportByBranch:
    plan_date: date
    meal_plans: list[DayMealPlan]
    branches: list[BranchUnits]