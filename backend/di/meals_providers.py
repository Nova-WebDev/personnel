from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client
from app.events.redis_event_publisher import RedisEventPublisher
from app.images.image_format_validator import ImageFormatValidator
from app.images.local_image_processor import LocalImageProcessor

from meals.infrastructure.cache.redis_cache_store import RedisCacheStore
from meals.infrastructure.data.repositories.meal_plan_time_policy_repository import MealPlanTimePolicyRepository
from meals.infrastructure.data.repositories.meal_repository import MealRepository

from meals.core.use_cases.set_meal_plan_time_policies import SetMealPlanTimePolicies
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.core.use_cases.create_meal import CreateMeal



async def get_set_meal_plan_time_policies_uc(session: AsyncSession) -> SetMealPlanTimePolicies:
    redis = await redis_client.get_client()
    return SetMealPlanTimePolicies(
        policy_repository=MealPlanTimePolicyRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        cache_store=RedisCacheStore(redis),
    )


async def get_meal_plan_time_policies_uc(session: AsyncSession) -> GetMealPlanTimePolicies:
    redis = await redis_client.get_client()
    return GetMealPlanTimePolicies(
        policy_repository=MealPlanTimePolicyRepository(session),
        cache_store=RedisCacheStore(redis),
    )




def get_create_meal_uc(session: AsyncSession) -> CreateMeal:
    return CreateMeal(
        meal_repository=MealRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        format_validator=ImageFormatValidator(),
        image_processor=LocalImageProcessor(),
    )