from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client
from app.events.redis_event_publisher import RedisEventPublisher
from app.images.image_format_validator import ImageFormatValidator
from app.images.local_image_processor import LocalImageProcessor

from meals.infrastructure.cache.redis_meal_cache import RedisMealCache
from meals.infrastructure.cache.redis_time_policy_cache import RedisTimePolicyCache
from meals.infrastructure.data.repositories.meal_plan_time_policy_repository import MealPlanTimePolicyRepository
from meals.infrastructure.data.repositories.meal_repository import MealRepository
from meals.infrastructure.data.repositories.meal_plan_repository import MealPlanRepository
from meals.infrastructure.data.repositories.meal_plan_recurring_repository import MealPlanRecurringRepository
from meals.infrastructure.data.repositories.voucher_repository import VoucherRepository

from user.infrastructure.data.repositories.permission_repository import PermissionRepository

from meals.core.use_cases.set_meal_plan_time_policies import SetMealPlanTimePolicies
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.core.use_cases.create_meal import CreateMeal
from meals.core.use_cases.update_meal import UpdateMeal
from meals.core.use_cases.set_meal_active_status import SetMealActiveStatus
from meals.core.use_cases.get_meals import GetMeals
from meals.core.use_cases.create_meal_plan import CreateMealPlan
from meals.core.use_cases.update_meal_plan import UpdateMealPlan
from meals.core.use_cases.delete_meal_plan import DeleteMealPlan
from meals.core.use_cases.get_meal_plans import GetMealPlans
from meals.core.use_cases.get_meal_photo import GetMealPhoto
from meals.core.use_cases.set_meal_plan_recurring import SetMealPlanRecurring
from meals.core.use_cases.get_meal_plan_recurring import GetMealPlanRecurring
from meals.core.use_cases.apply_recurring_cycle import ApplyRecurringCycle
from meals.core.use_cases.run_meal_plan_recurring_cron import RunMealPlanRecurringCron
from meals.core.use_cases.reserve_meal import ReserveMeal
from meals.core.use_cases.cancel_reservation import CancelReservation
from meals.core.use_cases.get_day_reservation_report import GetDayReservationReport
from meals.core.use_cases.get_day_reservation_report_by_branch import GetDayReservationReportByBranch
from meals.core.use_cases.bulk_reserve_meal import BulkReserveMeal



async def get_set_meal_plan_time_policies_uc(session: AsyncSession) -> SetMealPlanTimePolicies:
    redis = await redis_client.get_client()
    return SetMealPlanTimePolicies(
        policy_repository=MealPlanTimePolicyRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        time_policy_cache=RedisTimePolicyCache(redis),
    )


async def get_meal_plan_time_policies_uc(session: AsyncSession) -> GetMealPlanTimePolicies:
    redis = await redis_client.get_client()
    return GetMealPlanTimePolicies(
        policy_repository=MealPlanTimePolicyRepository(session),
        time_policy_cache=RedisTimePolicyCache(redis),
    )


async def get_create_meal_uc(session: AsyncSession) -> CreateMeal:
    redis = await redis_client.get_client()
    return CreateMeal(
        meal_repository=MealRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        format_validator=ImageFormatValidator(),
        image_processor=LocalImageProcessor(),
        meal_cache=RedisMealCache(redis),
    )


async def get_update_meal_uc(session: AsyncSession) -> UpdateMeal:
    redis = await redis_client.get_client()
    return UpdateMeal(
        meal_repository=MealRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        meal_cache=RedisMealCache(redis),
        format_validator=ImageFormatValidator(),
        image_processor=LocalImageProcessor(),
    )

async def get_set_meal_active_status_uc(session: AsyncSession) -> SetMealActiveStatus:
    redis = await redis_client.get_client()
    return SetMealActiveStatus(
        meal_repository=MealRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        meal_cache=RedisMealCache(redis),
    )


async def get_meals_uc(session: AsyncSession) -> GetMeals:
    redis = await redis_client.get_client()
    return GetMeals(
        meal_repository=MealRepository(session),
        meal_cache=RedisMealCache(redis),
    )



async def get_create_meal_plan_uc(session: AsyncSession) -> CreateMealPlan:
    return CreateMealPlan(
        meal_plan_repository=MealPlanRepository(session),
        get_time_policies=await get_meal_plan_time_policies_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )



async def get_update_meal_plan_uc(session: AsyncSession) -> UpdateMealPlan:
    return UpdateMealPlan(
        meal_plan_repository=MealPlanRepository(session),
        get_time_policies=await get_meal_plan_time_policies_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )


async def get_delete_meal_plan_uc(session: AsyncSession) -> DeleteMealPlan:
    return DeleteMealPlan(
        meal_plan_repository=MealPlanRepository(session),
        get_time_policies=await get_meal_plan_time_policies_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )

def get_meal_plans_uc(session: AsyncSession) -> GetMealPlans:
    return GetMealPlans(meal_plan_repository=MealPlanRepository(session))

def get_meal_photo_uc() -> GetMealPhoto:
    return GetMealPhoto(image_processor=LocalImageProcessor())






async def get_apply_recurring_cycle_uc(session: AsyncSession) -> ApplyRecurringCycle:
    return ApplyRecurringCycle(
        meal_plan_repository=MealPlanRepository(session),
        get_time_policies=await get_meal_plan_time_policies_uc(session),
    )


async def get_set_meal_plan_recurring_uc(session: AsyncSession) -> SetMealPlanRecurring:
    return SetMealPlanRecurring(
        recurring_repository=MealPlanRecurringRepository(session),
        meal_repository=MealRepository(session),
        permission_repository=PermissionRepository(session),
        apply_recurring_cycle=await get_apply_recurring_cycle_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )


async def get_run_meal_plan_recurring_cron_uc(session: AsyncSession) -> RunMealPlanRecurringCron:
    return RunMealPlanRecurringCron(
        recurring_repository=MealPlanRecurringRepository(session),
        meal_repository=MealRepository(session),
        apply_recurring_cycle=await get_apply_recurring_cycle_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )

def get_meal_plan_recurring_uc(session: AsyncSession) -> GetMealPlanRecurring:
    return GetMealPlanRecurring(recurring_repository=MealPlanRecurringRepository(session))


async def get_reserve_meal_uc(session: AsyncSession) -> ReserveMeal:
    return ReserveMeal(
        voucher_repository=VoucherRepository(session),
        permission_repository=PermissionRepository(session),
        get_time_policies=await get_meal_plan_time_policies_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )



async def get_cancel_reservation_uc(session: AsyncSession) -> CancelReservation:
    return CancelReservation(
        voucher_repository=VoucherRepository(session),
        permission_repository=PermissionRepository(session),
        get_time_policies=await get_meal_plan_time_policies_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )


def get_day_reservation_report_uc(session: AsyncSession) -> GetDayReservationReport:
    return GetDayReservationReport(voucher_repository=VoucherRepository(session))



def get_day_reservation_report_by_branch_uc(session: AsyncSession) -> GetDayReservationReportByBranch:
    return GetDayReservationReportByBranch(voucher_repository=VoucherRepository(session))



async def get_bulk_reserve_meal_uc(session: AsyncSession) -> BulkReserveMeal:
    return BulkReserveMeal(
        voucher_repository=VoucherRepository(session),
        permission_repository=PermissionRepository(session),
        get_time_policies=await get_meal_plan_time_policies_uc(session),
        event_publisher=RedisEventPublisher(redis_client),
    )