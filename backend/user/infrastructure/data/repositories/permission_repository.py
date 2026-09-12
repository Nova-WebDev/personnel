import uuid

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.core.entities.permission_level import PermissionLevel
from user.core.entities.permission_with_user import PermissionWithUser
from user.core.entities.scope_info import ScopeInfo
from user.core.interfaces.permission_repository import IPermissionRepository
from user.infrastructure.data.models.branch import BranchModel
from user.infrastructure.data.models.permission import PermissionModel
from user.infrastructure.data.models.unit import UnitModel
from user.infrastructure.data.models.user import UserModel


class PermissionRepository(IPermissionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_admin_user_ids(self) -> list[str]:
        stmt = select(PermissionModel.user_id).where(
            PermissionModel.level == PermissionLevel.ADMIN
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_global_and_branch_scoped_user_ids(self, branch_id: str) -> list[str]:
        branch_unit_ids = select(UnitModel.id).where(UnitModel.branch_id == branch_id)

        stmt = select(PermissionModel.user_id).where(
            (PermissionModel.group_id.is_(None))
            | (PermissionModel.group_id.in_(branch_unit_ids))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_global_and_unit_scoped_user_ids(self, unit_id: str) -> list[str]:
        stmt = select(PermissionModel.user_id).where(
            (PermissionModel.group_id.is_(None))
            | (PermissionModel.group_id == unit_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_scopes_with_location(self, permissions: list[dict]) -> list[ScopeInfo]:
        unit_ids = list({p["scope"] for p in permissions if p["scope"] is not None})

        unit_map: dict[str, tuple[str, str, str]] = {}
        if unit_ids:
            stmt = (
                select(UnitModel.id, UnitModel.name, BranchModel.id, BranchModel.name)
                .join(BranchModel, UnitModel.branch_id == BranchModel.id)
                .where(UnitModel.id.in_(unit_ids))
            )
            result = await self._session.execute(stmt)
            for unit_id, unit_name, branch_id, branch_name in result.all():
                unit_map[unit_id] = (unit_name, branch_id, branch_name)

        scopes = []
        for p in permissions:
            unit_id = p["scope"]

            if unit_id is None:
                scopes.append(ScopeInfo(
                    level=p["level"],
                    unit_id=None,
                    unit_name=None,
                    branch_id=None,
                    branch_name=None,
                ))
                continue

            unit_name, branch_id, branch_name = unit_map.get(unit_id, (None, None, None))
            scopes.append(ScopeInfo(
                level=p["level"],
                unit_id=unit_id,
                unit_name=unit_name,
                branch_id=branch_id,
                branch_name=branch_name,
            ))

        return scopes

    async def get_all_with_user_and_location(self) -> list[PermissionWithUser]:
        stmt = (
            select(
                PermissionModel.id,
                PermissionModel.user_id,
                UserModel.first_name,
                UserModel.last_name,
                PermissionModel.level,
                PermissionModel.group_id,
                UnitModel.name,
                BranchModel.id,
                BranchModel.name,
            )
            .join(UserModel, PermissionModel.user_id == UserModel.id)
            .outerjoin(UnitModel, PermissionModel.group_id == UnitModel.id)
            .outerjoin(BranchModel, UnitModel.branch_id == BranchModel.id)
        )
        result = await self._session.execute(stmt)

        return [
            PermissionWithUser(
                permission_id=row[0],
                user_id=row[1],
                first_name=row[2],
                last_name=row[3],
                level=row[4].value,
                unit_id=row[5],
                unit_name=row[6],
                branch_id=row[7],
                branch_name=row[8],
            )
            for row in result.all()
        ]

    async def delete_all_by_user_id(self, user_id: str) -> None:
        stmt = sql_delete(PermissionModel).where(PermissionModel.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def replace_all_for_user(self, user_id: str, permissions: list[dict]) -> None:
        delete_stmt = sql_delete(PermissionModel).where(PermissionModel.user_id == user_id)
        await self._session.execute(delete_stmt)

        for p in permissions:
            model = PermissionModel(
                id=str(uuid.uuid4()),
                user_id=user_id,
                level=PermissionLevel(p["level"]),
                group_id=p.get("scope"),
            )
            self._session.add(model)

        await self._session.flush()