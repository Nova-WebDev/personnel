from user.core.interfaces.user_repository import IUserRepository
from user.core.entities.user_with_location import UserWithLocation


class GetPublicUserProfile:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> UserWithLocation:
        return await self.user_repository.get_by_id(user_id)