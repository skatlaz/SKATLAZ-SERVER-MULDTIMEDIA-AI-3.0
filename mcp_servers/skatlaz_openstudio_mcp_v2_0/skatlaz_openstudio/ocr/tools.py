from pathlib import Path
from PIL import Image


def ocr_image(image_path: str, lang: str = 'por') -> str:
    try:
        import pytesseract
        return pytesseract.image_to_string(Image.open(image_path), lang=lang)
    except Exception as e:
        return f"OCR indisponivel ou Tesseract nao instalado: {e}"


def read_qrcode_barcode(image_path: str) -> list[dict]:
    try:
        from pyzbar.pyzbar import decode
        img = Image.open(image_path)
        return [{"type": d.type, "data": d.data.decode('utf-8', errors='ignore')} for d in decode(img)]
    except Exception as e:
        return [{"error": str(e)}]
