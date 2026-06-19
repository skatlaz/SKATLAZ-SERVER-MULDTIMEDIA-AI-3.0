from __future__ import annotations
import asyncio
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from .core.webtools import analyze_url, export_results_csv
from .core.screenshots import screenshot_url
from .core.reports import make_docx_report, make_xlsx_report
from .core.ocr import ocr_image, read_qr_barcode, create_qrcode

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"
SCREEN = BASE / "screenshots"
REPORTS = BASE / "reports"
UPLOADS = BASE / "data" / "uploads"
for p in [OUT, SCREEN, REPORTS, UPLOADS]:
    p.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Skatlaz SurfTask MCP", version="1.0")

class UrlRequest(BaseModel):
    url: str
    screenshot: bool = True
    report: bool = True

class MultiUrlRequest(BaseModel):
    urls: list[str]
    screenshot: bool = False

class QRRequest(BaseModel):
    text: str
    filename: str = "qrcode.png"

@app.get("/")
def root():
    return {"name":"Skatlaz SurfTask MCP", "tools":["web.analyze", "web.screenshot", "web.batch", "ocr.image", "barcode.read", "qrcode.create"]}

@app.post("/mcp/web/analyze")
async def mcp_web_analyze(req: UrlRequest):
    page = analyze_url(req.url, OUT)
    if req.screenshot:
        try:
            page["thumbnail"] = await screenshot_url(req.url, SCREEN)
        except Exception as e:
            page["thumbnail_error"] = str(e)
    if req.report:
        page["docx_report"] = make_docx_report(page, REPORTS / "site_report.docx")
    return page

@app.post("/mcp/web/batch")
async def mcp_web_batch(req: MultiUrlRequest):
    results = []
    for url in req.urls:
        try:
            page = analyze_url(url, OUT)
            if req.screenshot:
                try:
                    page["thumbnail"] = await screenshot_url(url, SCREEN)
                except Exception as e:
                    page["thumbnail_error"] = str(e)
            results.append(page)
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    csv = export_results_csv(results, REPORTS / "batch_sites.csv")
    xlsx = make_xlsx_report(results, REPORTS / "batch_sites.xlsx")
    return {"results": results, "csv": csv, "xlsx": xlsx}

@app.get("/mcp/web/screenshot")
async def mcp_screenshot(url: str):
    return {"thumbnail": await screenshot_url(url, SCREEN)}

@app.post("/mcp/ocr/image")
async def mcp_ocr_image(file: UploadFile = File(...)):
    path = UPLOADS / file.filename
    path.write_bytes(await file.read())
    return {"file": str(path), "text": ocr_image(str(path))}

@app.post("/mcp/barcode/read")
async def mcp_barcode_read(file: UploadFile = File(...)):
    path = UPLOADS / file.filename
    path.write_bytes(await file.read())
    return {"file": str(path), "codes": read_qr_barcode(str(path))}

@app.post("/mcp/qrcode/create")
def mcp_qr_create(req: QRRequest):
    path = REPORTS / req.filename
    return {"qrcode": create_qrcode(req.text, str(path))}
