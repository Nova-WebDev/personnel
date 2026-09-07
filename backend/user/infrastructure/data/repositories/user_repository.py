from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from user.core.errors.user_errors import (
    UnitNotFoundError,
    PhoneConflictError,
    PersonnelCodeConflictError,
    UserNotFoundError,
)
from user.core.interfaces.user_repository import IUserRepository
from user.infrastructure.data.models.user import UserModel
from user.infrastructure.data.models.unit import UnitModel
from user.infrastructure.data.models.branch import BranchModel
from user.core.entities.user_with_location import UserWithLocation


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_ids_by_branch(self, branch_id: str) -> list[str]:
        stmt = (
            select(UserModel.id)
            .join(UnitModel, UserModel.unit_id == UnitModel.id)
            .where(UnitModel.branch_id == branch_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_ids_by_unit(self, unit_id: str) -> list[str]:
        stmt = select(UserModel.id).where(UserModel.unit_id == unit_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_with_location(self) -> list[UserWithLocation]:
        stmt = self._select_with_location()
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.all()]

    async def get_by_unit_ids_with_location(self, unit_ids: list[str]) -> list[UserWithLocation]:
        stmt = self._select_with_location().where(UserModel.unit_id.in_(unit_ids))
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.all()]

    async def create(
        self,
        user_id: str,
        phone: str,
        first_name: str,
        last_name: str,
        unit_id: str,
        personnel_code: str | None,
        photo_path: str | None,
    ) -> UserWithLocation:
        await self._validate_unit_exists(unit_id)
        await self._validate_phone_unique(phone)

        if personnel_code is not None:
            await self._validate_personnel_code_unique(personnel_code)

        model = UserModel(
            id=user_id,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            unit_id=unit_id,
            personnel_code=personnel_code,
            photo_path=photo_path,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)

        stmt = self._select_with_location().where(UserModel.id == model.id)
        result = await self._session.execute(stmt)
        row = result.one()

        return self._to_entity(row)

    async def update(
        self,
        user_id: str,
        phone: str,
        first_name: str,
        last_name: str,
        unit_id: str,
        personnel_code: str | None,
    ) -> tuple[UserWithLocation, str | None]:
        model = await self._session.get(UserModel, user_id)

        if model is None:
            raise UserNotFoundError()

        previous_photo_path = model.photo_path

        if phone != model.phone:
            await self._validate_phone_unique(phone)

        if personnel_code != model.personnel_code and personnel_code is not None:
            await self._validate_personnel_code_unique(personnel_code)

        if unit_id != model.unit_id:
            await self._validate_unit_exists(unit_id)

        model.phone = phone
        model.first_name = first_name
        model.last_name = last_name
        model.unit_id = unit_id
        model.personnel_code = personnel_code

        await self._session.flush()
        await self._session.refresh(model)

        stmt = self._select_with_location().where(UserModel.id == model.id)
        result = await self._session.execute(stmt)
        row = result.one()

        return self._to_entity(row), previous_photo_path

    async def set_photo_path(self, user_id: str, photo_path: str) -> None:
        stmt = update(UserModel).where(UserModel.id == user_id).values(photo_path=photo_path)
        await self._session.execute(stmt)
        await self._session.flush()

    @staticmethod
    def _select_with_location():
        return (
            select(UserModel, UnitModel.name, BranchModel.id, BranchModel.name)
            .outerjoin(UnitModel, UserModel.unit_id == UnitModel.id)
            .outerjoin(BranchModel, UnitModel.branch_id == BranchModel.id)
        )

    @staticmethod
    def _to_entity(row) -> UserWithLocation:
        user, unit_name, branch_id, branch_name = row

        return UserWithLocation(
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
            unit_name=unit_name,
            branch_id=branch_id,
            branch_name=branch_name,
        )

    async def _validate_unit_exists(self, unit_id: str) -> None:
        unit = await self._session.get(UnitModel, unit_id)
        if unit is None:
            raise UnitNotFoundError()

    async def _validate_phone_unique(self, phone: str) -> None:
        stmt = select(UserModel.id).where(UserModel.phone == phone)
        result = await self._session.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise PhoneConflictError()

    async def _validate_personnel_code_unique(self, personnel_code: str) -> None:
        stmt = select(UserModel.id).where(UserModel.personnel_code == personnel_code)
        result = await self._session.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise PersonnelCodeConflictError()