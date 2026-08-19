from personnel.core.errors.personnel_errors import InvalidPhotoFileError
from personnel.core.interfaces.image_format_validator import IImageFormatValidator


class ImageFormatValidator(IImageFormatValidator):
    async def validate(self, file_bytes: bytes) -> None:
        if not file_bytes or len(file_bytes) < 4:
            raise InvalidPhotoFileError()

        if file_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            return
        if file_bytes.startswith(b"\xff\xd8"):
            return
        if file_bytes.startswith(b"GIF87a") or file_bytes.startswith(b"GIF89a"):
            return
        if file_bytes.startswith(b"RIFF") and b"WEBP" in file_bytes[:12]:
            return
        if file_bytes.startswith(b"BM"):
            return

        raise InvalidPhotoFileError()