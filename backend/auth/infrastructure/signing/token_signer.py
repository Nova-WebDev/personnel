from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from auth.core.interfaces.token_signer import ITokenSigner


class PrivateKeyLoader:
    _cache: dict[str, Ed25519PrivateKey] = {}

    @classmethod
    def load(cls, path: str) -> Ed25519PrivateKey:
        if path in cls._cache:
            return cls._cache[path]

        key_data = Path(path).read_bytes()
        cls._cache[path] = serialization.load_pem_private_key(key_data, password=None)
        return cls._cache[path]


class TokenSigner(ITokenSigner):
    def __init__(self, private_key_path: str = "auth/infrastructure/key/private_key.pem"):
        self.private_key = PrivateKeyLoader.load(private_key_path)

    async def sign(self, unsigned: str) -> bytes:
        unsigned_bytes = unsigned.encode("utf-8")
        return self.private_key.sign(unsigned_bytes)