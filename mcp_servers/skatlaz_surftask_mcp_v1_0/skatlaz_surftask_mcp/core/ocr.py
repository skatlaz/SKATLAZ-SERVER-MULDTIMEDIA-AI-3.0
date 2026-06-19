from __future__ import annotations
from pathlib import Path

def ocr_image(image_path: str) -> str:
    from PIL import Image
    import pytesseract
    return pytesseract.image_to_string(Image.open(image_path), lang="por+eng")

def read_qr_barcode(image_path: str) -> list[dict]:
    from PIL import Image
    from pyzbar.pyzbar import decode
    img = Image.open(image_path)
    out = []
    for code in decode(img):
        out.append({"type": code.type, "data": code.data.decode("utf-8", errors="ignore")})
    return out

def create_qrcode(text: str, output_path: str) -> str:
    import qrcode
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True)
    img = qrcode.make(text)
    img.save(path)
    return str(path)
