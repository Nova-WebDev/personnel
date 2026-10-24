from datetime import datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.entities.redeem_context import RedeemUser, RedeemVoucher
from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.voucher_repository import IVoucherRepository
from user.core.entities.permission_level import PermissionLevel
from user.core.interfaces.permission_repository import IPermissionRepository

NO_RESERVATION_MESSAGE = "This user has no meal reservation for today."
ALREADY_USED_MESSAGE = "This user's meal for today has already been used."
REDEEMED_MESSAGE = "Meal delivered and recorded successfully."


class RedeemMeal:
    def __init__(
        self,
        voucher_repository: IVoucherRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.voucher_repository = voucher_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, rfid_card_id: str, permissions: list[dict]) -> dict:
        self._authorize(permissions)

        today = datetime.now(timezone.utc).date()
        context = await self.voucher_repository.get_redeem_context(rfid_card_id, today)
        voucher = context.voucher

        if voucher is None:
            return self._result("no_reservation", NO_RESERVATION_MESSAGE, context.user, None)

        if voucher.is_used:
            return self._result("already_used", ALREADY_USED_MESSAGE, context.user, voucher)

        redeemed_at = await self.voucher_repository.mark_used(voucher.id)
        if redeemed_at is None:
            voucher.is_used = True
            return self._result("already_used", ALREADY_USED_MESSAGE, context.user, voucher)

        voucher.is_used = True
        voucher.redeemed_at = redeemed_at

        result = self._result("redeemed", REDEEMED_MESSAGE, context.user, voucher)
        await self._publish(context.user, result)

        return result

    async def _publish(self, user: RedeemUser, result: dict) -> None:
        unit_ids = [user.unit_id] if user.unit_id is not None else []
        recipients = await self.permission_repository.get_reservation_event_recipients(unit_ids)

        await self.event_publisher.publish(
            event="voucher.redeemed",
            scope="voucher",
            data={"user": result["user"], "voucher": result["voucher"]},
            targets=recipients.for_unit(user.unit_id, user.id),
        )

    @staticmethod
    def _result(status: str, message: str, user: RedeemUser, voucher: RedeemVoucher | None) -> dict:
        return {
            "status": status,
            "message": message,
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "personnel_code": user.personnel_code,
                "rfid_card_id": user.rfid_card_id,
                "photo_path": user.photo_path,
                "is_blocked": user.is_blocked,
                "unit_id": user.unit_id,
                "unit_name": user.unit_name,
                "branch_id": user.branch_id,
                "branch_name": user.branch_name,
            },
            "voucher": None
            if voucher is None
            else {
                "id": voucher.id,
                "meal_plan_id": voucher.meal_plan_id,
                "reservation_date": voucher.plan_date.isoformat(),
                "is_used": voucher.is_used,
                "redeemed_at": voucher.redeemed_at.isoformat() if voucher.redeemed_at else None,
                "meal": {
                    "id": voucher.meal.id,
                    "title": voucher.meal.title,
                    "description": voucher.meal.description,
                    "photo_path": voucher.meal.photo_path,
                    "is_active": voucher.meal.is_active,
                },
            },
        }

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.KITCHEN.value for p in permissions):
            raise PermissionDeniedError("Kitchen permission required")