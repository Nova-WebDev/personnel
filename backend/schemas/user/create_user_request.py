from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    phone: str
    first_name: str
    last_name: str
    unit_id: str
    personnel_code: str | None = None
    photo_path: str | None = None