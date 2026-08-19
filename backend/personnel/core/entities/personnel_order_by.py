from enum import Enum


class PersonnelOrderBy(str, Enum):
    PERSONNEL_ID = "personnel_id"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    BRANCH_ID = "branch_id"
    UNIT_ID = "unit_id"
    POSITION = "position"
    IS_BLOCKED = "is_blocked"
    CREATED_AT = "created_at"