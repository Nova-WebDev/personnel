from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client
from app.events.redis_event_publisher import RedisEventPublisher
from app.images.image_format_validator import ImageFormatValidator
from app.images.local_image_processor import LocalImageProcessor

from meals.infrastructure.cache.redis_meal_cache import RedisMealCache
from meals.infrastructure.cache.redis_time_policy_cache import RedisTimePolicyCache
from meals.infrastructure.data.repositories.meal_plan_time_policy_repository import MealPlanTimePolicyRepository
from meals.infrastructure.data.repositories.meal_repository import MealRepository
from user.infrastructure.data.repositories.permission_repository import PermissionRepository

from meals.core.use_cases.set_meal_plan_time_policies import SetMealPlanTimePolicies
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.core.use_cases.create_meal import CreateMeal
from meals.core.use_cases.update_meal import UpdateMeal
from meals.core.use_cases.set_meal_active_status import SetMealActiveStatus
from meals.core.use_cases.get_meals import GetMeals



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