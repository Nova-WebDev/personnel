import base64
import json
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from auth.key_loader import PublicKeyLoader
from auth.token_payload import TokenPayload
from settings import settings


class JWTDecodeError(Exception):
    pass


class JWTDecoder:
    def __init__(self, public_key_path: str = ""):
        self.public_key: Ed25519PublicKey = PublicKeyLoader.load(
            public_key_path or settings.public_key_path
        )

    def decode(self, token: str) -> TokenPayload:
        header_b64, payload_b64, signature_b64 = self._split_token(token)
        self._verify_signature(header_b64, payload_b64, signature_b64)
        payload = self._parse_payload(payload_b64)
        self._check_expiry(payload)
        return TokenPayload(public_id=self._read_user_id(payload), exp=payload["exp"])

    @staticmethod
    def _split_token(token: str) -> tuple[str, str, str]:
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")
        except ValueError:
            raise JWTDecodeError("Invalid token format")
        return header_b64, payload_b64, signature_b64

    def _verify_signature(self, header_b64: str, payload_b64: str, signature_b64: str) -> None:
        unsigned = f"{header_b64}.{payload_b64}".encode("utf-8")

        try:
            signature = self._b64decode(signature_b64)
        except ValueError as e:
            raise JWTDecodeError("Invalid signature encoding") from e

        try:
            self.public_key.verify(signature, unsigned)
        except InvalidSignature:
            raise JWTDecodeError("Invalid signature")

    def _parse_payload(self, payload_b64: str) -> dict:
        try:
            payload_raw = self._b64decode(payload_b64)
            payload = json.loads(payload_raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            raise JWTDecodeError("Invalid payload") from e

        if not isinstance(payload, dict):
            raise JWTDecodeError("Invalid payload")

        return payload

    @staticmethod
    def _check_expiry(payload: dict) -> None:
        exp = payload.get("exp")
        if not isinstance(exp, int) or exp < int(time.time()):
            raise JWTDecodeError("Token expired")

    @staticmethod
    def _read_user_id(payload: dict) -> str:
        user_id = payload.get("id")
        if not isinstance(user_id, str) or not user_id:
            raise JWTDecodeError("Missing id")

        return user_id

    @staticmethod
    def _b64decode(data: str) -> bytes:
        padding = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)
