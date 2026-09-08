import os
from PIL import Image

from app.settings import settings
from app.interfaces.image_processor import IImageProcessor


class LocalImageProcessor(IImageProcessor):
    def __init__(self):
        self.base_dir = settings.storage_path

    def _folder_path(self, folder: str) -> str:
        path = os.path.join(self.base_dir, folder)
        os.makedirs(path, exist_ok=True)
        return path

    async def process(
        self,
        folder: str,
        file_id: str,
        file_bytes: bytes,
        resize_to: tuple[int, int] | None = None,
        force_png: bool = True,
    ) -> None:
        path = os.path.join(self._folder_path(folder), file_id)

        with open(path, "wb") as f:
            f.write(file_bytes)

        with Image.open(path) as img:
            orig_w, orig_h = img.size

            if resize_to is not None:
                target_w, target_h = resize_to
                target_ratio = target_w / target_h
                orig_ratio = orig_w / orig_h

                if orig_ratio > target_ratio:
                    new_w = int(orig_h * target_ratio)
                    offset = (orig_w - new_w) // 2
                    img = img.crop((offset, 0, offset + new_w, orig_h))
                elif orig_ratio < target_ratio:
                    new_h = int(orig_w / target_ratio)
                    offset = (orig_h - new_h) // 2
                    img = img.crop((0, offset, orig_w, offset + new_h))

                cropped_w, cropped_h = img.size
                if cropped_w > target_w or cropped_h > target_h:
                    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

            if force_png:
                img = img.convert("RGBA")
                img.save(path, format="PNG")
            else:
                img = img.convert("RGB")
                img.save(path, format="JPEG", quality=85)

    async def load(self, folder: str, file_id: str) -> bytes:
        path = os.path.join(self._folder_path(folder), file_id)
        with open(path, "rb") as f:
            return f.read()

    async def delete(self, folder: str, file_id: str) -> None:
        path = os.path.join(self._folder_path(folder), file_id)
        if os.path.exists(path):
            os.remove(path)

    async def exists(self, folder: str, file_id: str) -> bool:
        path = os.path.join(self._folder_path(folder), file_id)
        return os.path.exists(path)

    async def save_raw(self, folder: str, file_id: str, file_bytes: bytes) -> None:
        path = os.path.join(self._folder_path(folder), file_id)
        with open(path, "wb") as f:
            f.write(file_bytes)