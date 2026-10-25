from datetime import date, datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.entities.inviter_guest_row import InviterGuestRow
from meals.core.entities.redeem_context import RedeemUser, RedeemVoucher
from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.guest_repository import IGuestRepository
from meals.core.interfaces.voucher_repository import IVoucherRepository
from user.core.entities.permission_level import PermissionLevel
from user.core.interfaces.permission_repository import IPermissionRepository

NO_RESERVATION_MESSAGE = "This user has no meal reservation for today."
ALREADY_USED_MESSAGE = "This user's meal for today has already been used."
REDEEMED_MESSAGE = "Meal delivered and recorded successfully."
NO_GUESTS_MESSAGE = "This user has no guests for today."


class RedeemMeal:
    def __init__(
        self,
        voucher_repository: IVoucherRepository,
        guest_repository: IGuestRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.voucher_repository = voucher_repository
        self.guest_repository = guest_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, rfid_card_id: str, permissions: list[dict]) -> dict:
        self._authorize(permissions)

        today = datetime.now(timezone.utc).date()
        context = await self.voucher_repository.get_redeem_context(rfid_card_id, today)
        user = context.user
        voucher = context.voucher

        guest_rows = await self.guest_repository.get_inviter_guests(user.id, today)

        status, message, voucher_redeemed = await self._redeem_voucher(voucher)

        delivered: dict[str, int] = {}
        if any(not row.is_used for row in guest_rows):
            delivered = await self.guest_repository.mark_inviter_guests_used(user.id, today)

        result = self._result(status, message, user, voucher, self._summarize_guests(guest_rows, delivered))

        if voucher_redeemed or delivered:
            await self._publish(user, result)

        return result

    async def _redeem_voucher(self, voucher: RedeemVoucher | None) -> tuple[str, str, bool]:
        if voucher is None:
            return "no_reservation", NO_RESERVATION_MESSAGE, False

        if voucher.is_used:
            return "already_used", ALREADY_USED_MESSAGE, False

        redeemed_at = await self.voucher_repository.mark_used(voucher.id)
        voucher.is_used = True

        if redeemed_at is None:
            return "already_used", ALREADY_USED_MESSAGE, False

        voucher.redeemed_at = redeemed_at
        return "redeemed", REDEEMED_MESSAGE, True

    async def _publish(self, user: RedeemUser, result: dict) -> None:
        unit_ids = [user.unit_id] if user.unit_id is not None else []
        recipients = await self.permission_repository.get_reservation_event_recipients(unit_ids)

        await self.event_publisher.publish(
            event="voucher.redeemed",
            scope="voucher",
            data={"user": result["user"], "voucher": result["voucher"], "guests": result["guests"]},
            targets=recipients.for_unit(user.unit_id, user.id),
        )

    @staticmethod
    def _summarize_guests(rows: list[InviterGuestRow], delivered: dict[str, int]) -> dict:
        totals: dict[str, dict] = {}
        for row in rows:
            entry = totals.setdefault(
                row.meal_plan_id,
                {
                    "meal_plan_id": row.meal_plan_id,
                    "meal": {
                        "id": row.meal.id,
                        "title": row.meal.title,
                        "description": row.meal.description,
                        "photo_path": row.meal.photo_path,
                        "is_active": row.meal.is_active,
                    },
                    "total": 0,
                },
            )
            entry["total"] += row.guest_count

        by_meal = []
        for plan_id, entry in totals.items():
            delivered_now = delivered.get(plan_id, 0)
            by_meal.append(
                {
                    "meal_plan_id": plan_id,
                    "meal": entry["meal"],
                    "delivered_now": delivered_now,
                    "already_delivered": entry["total"] - delivered_now,
                }
            )

        total = sum(entry["total"] for entry in totals.values())
        delivered_now = sum(item["delivered_now"] for item in by_meal)
        already_delivered = total - delivered_now

        if total == 0:
            message = NO_GUESTS_MESSAGE
        elif delivered_now > 0 and already_delivered > 0:
            message = f"{delivered_now} guest meal(s) delivered now; {already_delivered} were already delivered."
        elif delivered_now > 0:
            message = f"{delivered_now} guest meal(s) delivered."
        else:
            message = f"All {total} guest meal(s) were already delivered."

        return {
            "message": message,
            "total": total,
            "delivered_now": delivered_now,
            "already_delivered": already_delivered,
            "by_meal": by_meal,
        }

    @staticmethod
    def _result(
        status: str, message: str, user: RedeemUser, voucher: RedeemVoucher | None, guests: dict
    ) -> dict:
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
            "guests": guests,
        }

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.KITCHEN.value for p in permissions):
            raise PermissionDeniedError("Kitchen permission required")