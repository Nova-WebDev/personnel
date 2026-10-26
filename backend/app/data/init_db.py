from sqlalchemy import text

from app.data.base import Base
from app.data.db import engine

INIT_DB_LOCK_ID = 727001


def _load_models():
    from meals.infrastructure.data.models.guest_reservation import GuestReservationModel  # noqa
    from meals.infrastructure.data.models.meal import MealModel  # noqa
    from meals.infrastructure.data.models.meal_plan import MealPlanModel  # noqa
    from meals.infrastructure.data.models.meal_plan_recurring import MealPlanRecurringModel  # noqa
    from meals.infrastructure.data.models.meal_plan_time_policy import MealPlanTimePolicyModel  # noqa
    from meals.infrastructure.data.models.voucher import VoucherModel  # noqa
    from user.infrastructure.data.models.branch import BranchModel  # noqa
    from user.infrastructure.data.models.permission import PermissionModel  # noqa
    from user.infrastructure.data.models.unit import UnitModel  # noqa
    from user.infrastructure.data.models.user import UserModel  # noqa


async def init_db():
    _load_models()
    async with engine.begin() as conn:
        await conn.execute(text("SELECT pg_advisory_xact_lock(:lock_id)"), {"lock_id": INIT_DB_LOCK_ID})
        await conn.run_sync(Base.metadata.create_all)