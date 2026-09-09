from user.core.interfaces.user_repository import IUserRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from user.core.entities.user_profile import UserProfile


class GetMyProfile:
    def __init__(self, user_repository: IUserRepository, permission_repository: IPermissionRepository):
        self.user_repository = user_repository
        self.permission_repository = permission_repository

    async def execute(self, user_id: str, permissions: list[dict]) -> UserProfile:
        user = await self.user_repository.get_by_id(user_id)
        scopes = await self.permission_repository.get_scopes_with_location(permissions)

        return UserProfile(
            id=user.id,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            personnel_code=user.personnel_code,
            rfid_card_id=user.rfid_card_id,
            photo_path=user.photo_path,
            is_blocked=user.is_blocked,
            created_at=user.created_at,
            unit_id=user.unit_id,
            unit_name=user.unit_name,
            branch_id=user.branch_id,
            branch_name=user.branch_name,
            scopes=scopes,
        )