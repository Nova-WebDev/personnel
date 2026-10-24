from app.interfaces.event_publisher import IEventPublisher
from user.core.entities.permission_level import PermissionLevel
from user.core.errors.user_errors import PermissionDeniedError
from user.core.interfaces.permission_repository import IPermissionRepository
from user.core.interfaces.user_repository import IUserRepository


class SetUserRfid:
    def __init__(
        self,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.user_repository = user_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, user_id: str, rfid_card_id: str | None, permissions: list[dict]) -> None:
        current = await self.user_repository.get_by_id(user_id)
        self._authorize(current.unit_id, permissions)

        await self.user_repository.set_rfid_card(user_id, rfid_card_id)

        unit_ids = [current.unit_id] if current.unit_id is not None else []
        recipients = await self.permission_repository.get_reservation_event_recipients(unit_ids)
        targets = recipients.for_unit(current.unit_id, user_id)

        hr_ids = await self.permission_repository.get_hr_manager_user_ids(current.unit_id)
        targets = list(set(targets) | set(hr_ids))

        await self.event_publisher.publish(
            event="user.rfid_updated",
            scope="user",
            data={"id": user_id, "has_rfid": rfid_card_id is not None},
            targets=targets,
        )

    @staticmethod
    def _authorize(unit_id: str | None, permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_hr_for_unit = unit_id is not None and any(
            p["level"] == PermissionLevel.HR_MANAGER.value and p["scope"] == unit_id for p in permissions
        )

        if not (is_admin or is_hr_for_unit):
            raise PermissionDeniedError()