from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import shutil

from skatlaz_openstudio.audio.tools import audio_info, apply_audio_effects
from skatlaz_openstudio.video.tools import video_info, apply_video_filter, create_thumbnail
from skatlaz_openstudio.image.tools import create_cover, apply_image_filter, create_qrcode
from skatlaz_openstudio.ocr.tools import ocr_image, read_qrcode_barcode
from skatlaz_openstudio.tts.tools import text_to_speech
from skatlaz_openstudio.subtitles.tools import create_srt
from skatlaz_openstudio.canvas.tools import render_template
from skatlaz_openstudio.web.tools import scrape_page
from skatlaz_openstudio.publishing import text_to_pdf, text_to_docx

app = FastAPI(title="Skatlaz OpenStudio MCP", version="2.0.0")
BASE = Path("workspace")
UPLOADS = BASE / "uploads"
OUTPUTS = BASE / "outputs"
UPLOADS.mkdir(parents=True, exist_ok=True)
OUTPUTS.mkdir(parents=True, exist_ok=True)

class TextPayload(BaseModel):
    text: str
    output_name: str = "output.mp3"
    lang: str = "pt"

class CoverPayload(BaseModel):
    title: str
    subtitle: str = ""
    output_name: str = "cover.png"

class UrlPayload(BaseModel):
    url: str

class SrtPayload(BaseModel):
    lines: list[str]
    output_name: str = "subtitles.srt"
    seconds_per_line: int = 4

class CanvasPayload(BaseModel):
    title: str
    subtitle: str = ""
    items: list[dict] = []
    output_name: str = "canvas.html"

@app.get("/")
def root():
    return {"name":"Skatlaz OpenStudio MCP", "version":"2.0.0", "status":"ok"}

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    dest = UPLOADS / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"file": str(dest)}

@app.post("/audio/info")
def api_audio_info(path: str):
    return audio_info(path)

@app.post("/audio/effects")
def api_audio_effects(input_path: str, output_name: str = "audio_master.mp3", normalize: bool = True, gain_db: float = 0):
    out = OUTPUTS / output_name
    return {"output": apply_audio_effects(input_path, str(out), normalize=normalize, gain_db=gain_db)}

@app.post("/tts")
def api_tts(payload: TextPayload):
    out = OUTPUTS / payload.output_name
    return {"output": text_to_speech(payload.text, str(out), payload.lang)}

@app.post("/video/info")
def api_video_info(path: str):
    return video_info(path)

@app.post("/video/filter")
def api_video_filter(input_path: str, output_name: str = "video_filtered.mp4", filter_name: str = "gray"):
    out = OUTPUTS / output_name
    return {"output": apply_video_filter(input_path, str(out), filter_name)}

@app.post("/video/thumbnail")
def api_thumbnail(input_path: str, output_name: str = "thumbnail.jpg", time_sec: float = 1.0):
    out = OUTPUTS / output_name
    return {"output": create_thumbnail(input_path, str(out), time_sec)}

@app.post("/image/cover")
def api_cover(payload: CoverPayload):
    out = OUTPUTS / payload.output_name
    return {"output": create_cover(payload.title, payload.subtitle, str(out))}

@app.post("/image/filter")
def api_image_filter(input_path: str, output_name: str = "image_filtered.png", filter_name: str = "sharpen"):
    out = OUTPUTS / output_name
    return {"output": apply_image_filter(input_path, str(out), filter_name)}

@app.post("/qrcode")
def api_qrcode(data: str, output_name: str = "qrcode.png"):
    out = OUTPUTS / output_name
    return {"output": create_qrcode(data, str(out))}

@app.post("/ocr/image")
def api_ocr(path: str, lang: str = "por"):
    return {"text": ocr_image(path, lang)}

@app.post("/ocr/barcode")
def api_barcode(path: str):
    return {"codes": read_qrcode_barcode(path)}

@app.post("/subtitles/srt")
def api_srt(payload: SrtPayload):
    out = OUTPUTS / payload.output_name
    return {"output": create_srt(payload.lines, str(out), payload.seconds_per_line)}

@app.post("/canvas/render")
def api_canvas(payload: CanvasPayload):
    out = OUTPUTS / payload.output_name
    return {"output": render_template(str(out), payload.title, payload.subtitle, payload.items)}

@app.post("/web/scrape")
def api_scrape(payload: UrlPayload):
    return scrape_page(payload.url)

@app.post("/publish/pdf")
def api_pdf(text: str, output_name: str = "document.pdf", title: str = "Skatlaz OpenStudio"):
    out = OUTPUTS / output_name
    return {"output": text_to_pdf(text, str(out), title)}

@app.post("/publish/docx")
def api_docx(text: str, output_name: str = "document.docx", title: str = "Skatlaz OpenStudio"):
    out = OUTPUTS / output_name
    return {"output": text_to_docx(text, str(out), title)}
