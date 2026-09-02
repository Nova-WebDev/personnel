from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


class PublicKeyLoader:
    _cache: dict[str, Ed25519PublicKey] = {}

    @classmethod
    def load(cls, path: str) -> Ed25519PublicKey:
        if path in cls._cache:
            return cls._cache[path]

        key_data = Path(path).read_bytes()
        cls._cache[path] = serialization.load_pem_public_key(key_data)
        return cls._cache[path]