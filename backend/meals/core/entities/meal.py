from dataclasses import dataclass

@dataclass
class Meal:
    id: str
    title: str
    description: str | None
    photo_path: str | None
    is_active: bool