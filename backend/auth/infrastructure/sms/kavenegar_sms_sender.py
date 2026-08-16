import httpx

from auth.core.interfaces.sms_sender import ISmsSender
from app.settings import settings


class KavenegarSmsSender(ISmsSender):
    def __init__(self):
        self.url = (
            f"https://api.kavenegar.com/v1/"
            f"{settings.sms_api_key}/verify/lookup.json"
        )
        self.template = settings.sms_template

    async def send(self, phone_number: str, code: str):
        params = {
            "receptor": phone_number,
            "token": code,
            "template": self.template,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                self.url,
                params=params,
            )

            response.raise_for_status()