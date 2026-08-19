import uuid
from abc import ABC, abstractmethod

from personnel.core.entities.branch_entity import BranchEntity
from personnel.core.entities.unit_entity import UnitEntity
from personnel.core.entities.branch_with_units_entity import BranchWithUnitsEntity
from personnel.core.entities.personnel_entity import PersonnelEntity
from personnel.core.entities.position import PersonnelPosition
from personnel.core.entities.personnel_order_by import PersonnelOrderBy
from personnel.core.entities.personnel_detail_entity import PersonnelDetailEntity

class IPersonnelRepository(ABC):
    @abstractmethod
    async def create_branch(self, name: str) -> BranchEntity:
        pass

    @abstractmethod
    async def create_unit(self, name: str, branch_id: int) -> UnitEntity:
        pass

    @abstractmethod
    async def update_branch(self, branch_id: int, name: str) -> BranchEntity:
        pass

    @abstractmethod
    async def delete_branch(self, branch_id: int) -> None:
        pass

    @abstractmethod
    async def update_unit_name(self, unit_id: int, name: str) -> None:
        pass

    @abstractmethod
    async def delete_unit(self, unit_id: int) -> None:
        pass

    @abstractmethod
    async def get_all_branches_with_units(self) -> list[BranchWithUnitsEntity]:
        pass

    @abstractmethod
    async def create_personnel(
            self,
            personnel_id: str,
            first_name: str,
            last_name: str,
            branch_id: int,
            unit_id: int | None,
            photo_path: str | None,
            position: PersonnelPosition | None,
    ) -> PersonnelEntity:
        pass

    @abstractmethod
    async def update_personnel(
            self,
            personnel_uuid: uuid.UUID,
            personnel_id: str,
            first_name: str,
            last_name: str,
            branch_id: int,
            unit_id: int | None,
            position: PersonnelPosition | None,
            photo_path: str | None,
    ) -> PersonnelEntity:
        pass

    @abstractmethod
    async def set_personnel_block_status(self, personnel_uuid: uuid.UUID, is_blocked: bool) -> None:
        pass

    @abstractmethod
    async def count_personnel(self, search: str | None) -> int:
        pass

    @abstractmethod
    async def get_personnel_paginated(
            self,
            offset: int,
            limit: int,
            search: str | None,
            order_by: PersonnelOrderBy,
            descending: bool,
    ) -> list[PersonnelEntity]:
        pass

    @abstractmethod
    async def update_photo_path(self, personnel_uuid: uuid.UUID, photo_path: str) -> None:
        pass

    @abstractmethod
    async def get_by_uuid(self, personnel_uuid: uuid.UUID) -> PersonnelEntity | None:
        pass

    @abstractmethod
    async def get_personnel_detail(self, personnel_uuid: uuid.UUID) -> PersonnelDetailEntity | None:
        pass