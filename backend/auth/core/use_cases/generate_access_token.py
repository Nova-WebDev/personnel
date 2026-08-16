import time
from dataclasses import asdict

from auth.core.entities.auth_session_entity import AuthSessionEntity
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

    async def execute(self, data: AuthSessionEntity) -> str:
        now = int(time.time())

        header = await self.header_generator.generate_header()

        payload = await self.payload_generator.generate_payload({
            "phone_number": data.phone_number,
            "public_id": data.public_id,
            "role": data.role,
            "iat": now
        })

        header_b64 = encode_json(asdict(header))
        payload_b64 = encode_json(asdict(payload))
        unsigned = f"{header_b64}.{payload_b64}"

        signature = await self.signer.sign(unsigned)
        signature_b64 = encode_bytes(signature)

        return f"{unsigned}.{signature_b64}"
