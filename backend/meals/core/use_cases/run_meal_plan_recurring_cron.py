from datetime import datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.interfaces.meal_plan_recurring_repository import IMealPlanRecurringRepository
from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.use_cases.apply_recurring_cycle import ApplyRecurringCycle
from meals.utility.recurring_cycle import advance


class RunMealPlanRecurringCron:
    def __init__(
        self,
        recurring_repository: IMealPlanRecurringRepository,
        meal_repository: IMealRepository,
        apply_recurring_cycle: ApplyRecurringCycle,
        event_publisher: IEventPublisher,
    ):
        self.recurring_repository = recurring_repository
        self.meal_repository = meal_repository
        self.apply_recurring_cycle = apply_recurring_cycle
        self.event_publisher = event_publisher

    async def execute(self) -> None:
        now = datetime.now(timezone.utc)

        cycle = await self.recurring_repository.get_all()
        items = [{"target_date": c.target_date, "meal_id": c.meal_id} for c in cycle]

        result = advance(items, now.date())
        if not result.visited:
            return

        meal_ids = list({m for _, m in result.visited if m is not None})
        statuses = await self.meal_repository.get_active_statuses(meal_ids)

        applied = await self.apply_recurring_cycle.execute(result.visited, statuses, now)
        await self.recurring_repository.replace_all(result.rotated)

        if applied:
            await self.event_publisher.publish(
                event="meal_plan.recurring_applied",
                scope="meal_plan",
                data={"days": [self.apply_recurring_cycle.serialize_day(day) for day in applied]},
                targets=["*"],
            )