import json

from meals.core.interfaces.meal_plan_time_policy_repository import IMealPlanTimePolicyRepository
from meals.core.interfaces.time_policy_cache import ITimePolicyCache
from meals.core.entities.week_day import WeekDay
from meals.core.errors.meals_errors import PermissionDeniedError, InvalidTimePolicyError
from app.interfaces.event_publisher import IEventPublisher
from user.core.entities.permission_level import PermissionLevel


class SetMealPlanTimePolicies:
    def __init__(
        self,
        policy_repository: IMealPlanTimePolicyRepository,
        event_publisher: IEventPublisher,
        time_policy_cache: ITimePolicyCache,
    ):
        self.policy_repository = policy_repository
        self.event_publisher = event_publisher
        self.time_policy_cache = time_policy_cache

    async def execute(self, policies: list[dict], permissions: list[dict]) -> None:
        self._authorize(permissions)
        self._validate(policies)

        result = await self.policy_repository.upsert_all(policies)

        payload = [
            {"id": p.id, "target_weekday": p.target_weekday.value, "cutoff_hours_before": p.cutoff_hours_before}
            for p in result
        ]

        await self.time_policy_cache.clear()
        await self.time_policy_cache.set_all(json.dumps(payload))

        await self.event_publisher.publish(
            event="meal_plan_time_policy.updated",
            scope="meal_plan_time_policy",
            data={"policies": payload},
            targets=["*"],
        )

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)

        if not is_admin:
            raise PermissionDeniedError()

    @staticmethod
    def _validate(policies: list[dict]) -> None:
        weekdays = [p["target_weekday"] for p in policies]

        if sorted(weekdays) != sorted(day.value for day in WeekDay):
            raise InvalidTimePolicyError()