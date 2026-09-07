from user.core.interfaces.user_repository import IUserRepository
from user.core.entities.user_with_location import UserWithLocation


class GetUsersWithLocation:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, permissions: list[dict]) -> list[UserWithLocation]:
        has_global_permission = any(p["scope"] is None for p in permissions)

        if has_global_permission:
            return await self.user_repository.get_all_with_location()

        unit_ids = list({p["scope"] for p in permissions if p["scope"] is not None})

        if not unit_ids:
            return []

        return await self.user_repository.get_by_unit_ids_with_location(unit_ids)