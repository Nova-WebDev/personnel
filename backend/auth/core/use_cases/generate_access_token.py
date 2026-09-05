import time
from dataclasses import asdict

from auth.core.entities.auth_session_entity import AuthSessionEntity
from auth.core.entities.access_token_result import AccessTokenResult
from auth.core.interfaces.token_header_generator import ITokenHeaderGenerator
from auth.core.interfaces.token_payload_generator import ITokenPayloadGenerator
from auth.core.interfaces.token_signer import ITokenSigner
from auth.utility.base64url import encode_json, encode_bytes


class GenerateAccessToken:
    def __init__(
        self,
        header_generator: ITokenHeaderGenerator,
        payload_generator: ITokenPayloadGenerator,
        signer: ITokenSigner
    ):
        self.header_generator = header_generator
        self.payload_generator = payload_generator
        self.signer = signer

    async def execute(self, data: AuthSessionEntity) -> AccessTokenResult:
        now = int(time.time())

        header = await self.header_generator.generate_header()

        payload = await self.payload_generator.generate_payload({
            "id": data.id,
            "phone_number": data.phone_number,
            "permissions": data.permissions,
            "iat": now
        })

        header_b64 = encode_json(asdict(header))
        payload_b64 = encode_json(asdict(payload))
        unsigned = f"{header_b64}.{payload_b64}"

        signature = await self.signer.sign(unsigned)
        signature_b64 = encode_bytes(signature)

        token = f"{unsigned}.{signature_b64}"

        return AccessTokenResult(token=token, expires_at=payload.exp)