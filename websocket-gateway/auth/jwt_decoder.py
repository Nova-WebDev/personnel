import base64
import json
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from auth.key_loader import PublicKeyLoader
from auth.token_payload import TokenPayload


class JWTDecodeError(Exception):
    pass


class JWTDecoder:
    def __init__(self, public_key_path: str = "key/public_key.pem"):
        self.public_key: Ed25519PublicKey = PublicKeyLoader.load(public_key_path)

    def decode(self, token: str) -> TokenPayload:
        header_b64, payload_b64, signature_b64 = self._split_token(token)
        self._verify_signature(header_b64, payload_b64, signature_b64)
        payload = self._parse_payload(payload_b64)
        self._check_expiry(payload)
        return TokenPayload(public_id=payload["public_id"])

    @staticmethod
    def _split_token(token: str) -> tuple[str, str, str]:
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")
        except ValueError:
            raise JWTDecodeError("Invalid token format")
        return header_b64, payload_b64, signature_b64

    def _verify_signature(self, header_b64: str, payload_b64: str, signature_b64: str) -> None:
        unsigned = f"{header_b64}.{payload_b64}".encode("utf-8")
        signature = self._b64decode(signature_b64)

        try:
            self.public_key.verify(signature, unsigned)
        except InvalidSignature:
            raise JWTDecodeError("Invalid signature")

    def _parse_payload(self, payload_b64: str) -> dict:
        try:
            payload_raw = self._b64decode(payload_b64)
            return json.loads(payload_raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            raise JWTDecodeError("Invalid payload") from e

    @staticmethod
    def _check_expiry(payload: dict) -> None:
        now = int(time.time())
        exp = payload.get("exp")
        if exp is None or exp < now:
            raise JWTDecodeError("Token expired")

    @staticmethod
    def _b64decode(data: str) -> bytes:
        padding = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)