from dataclasses import dataclass, field


@dataclass
class ReservationRecipients:
    global_user_ids: set[str] = field(default_factory=set)
    managers_by_unit: dict[str, set[str]] = field(default_factory=dict)

    def for_unit(self, unit_id: str | None, user_id: str) -> list[str]:
        managers = self.managers_by_unit.get(unit_id, set()) if unit_id is not None else set()
        return list(self.global_user_ids | managers | {user_id})