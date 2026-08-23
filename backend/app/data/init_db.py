from sqlalchemy import text

from app.data.db import engine
from app.data.base import Base

INIT_DB_LOCK_ID = 918273645


def _load_models():
    from auth.infrastructure.data.models import User # noqa
    from personnel.infrastructure.data.models import Personnel, Branch, Unit # noqa


async def init_db():
    _load_models()
    async with engine.begin() as conn:
        await conn.execute(text("SELECT pg_advisory_lock(:lock_id)"), {"lock_id": INIT_DB_LOCK_ID})
        try:
            await conn.run_sync(Base.metadata.create_all)
        finally:
            await conn.execute(text("SELECT pg_advisory_unlock(:lock_id)"), {"lock_id": INIT_DB_LOCK_ID})