import io

import qrcode

from personnel.core.interfaces.qr_code_generator import IQRCodeGenerator


class QRCodeGenerator(IQRCodeGenerator):
    async def generate(self, data: str) -> bytes:
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()