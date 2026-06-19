from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import qrcode


def apply_image_filter(input_path: str, output_path: str, filter_name: str = 'sharpen') -> str:
    img = Image.open(input_path).convert('RGB')
    if filter_name == 'blur':
        img = img.filter(ImageFilter.GaussianBlur(2))
    elif filter_name == 'sharpen':
        img = img.filter(ImageFilter.SHARPEN)
    elif filter_name == 'contrast':
        img = ImageEnhance.Contrast(img).enhance(1.4)
    elif filter_name == 'brightness':
        img = ImageEnhance.Brightness(img).enhance(1.2)
    elif filter_name == 'bw':
        img = img.convert('L').convert('RGB')
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path


def create_cover(title: str, subtitle: str, output_path: str, size=(1600, 2400), bg=(245,245,235), fg=(85,95,45)) -> str:
    img = Image.new('RGB', size, bg)
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype('arial.ttf', 96)
        font_sub = ImageFont.truetype('arial.ttf', 44)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    draw.rectangle([80,80,size[0]-80,size[1]-80], outline=fg, width=10)
    draw.text((140, 320), title, fill=fg, font=font_title)
    draw.text((140, 470), subtitle or '', fill=(120,90,40), font=font_sub)
    draw.text((140, size[1]-220), 'Skatlaz OpenStudio MCP', fill=fg, font=font_sub)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path


def create_qrcode(data: str, output_path: str) -> str:
    img = qrcode.make(data)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path
