from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import shutil, uuid

from skatlaz_office_worker.documents import read_document, summarize_text, correct_text_basic, write_txt
from skatlaz_office_worker.translator import translate_text_basic
from skatlaz_office_worker.spreadsheets import read_table, clean_table, apply_prompt_formula, create_chart, olap_summary, save_excel
from skatlaz_office_worker.slides import create_presentation
from skatlaz_office_worker.vision import ocr_image, read_codes, create_qrcode, describe_image_basic
from skatlaz_office_worker.web import read_url, extract_products_simple
from skatlaz_office_worker.security import sha256_file, encrypt_file, decrypt_file
from skatlaz_office_worker.canvas import create_report_html
from skatlaz_office_worker.sql import sqlite_query
from skatlaz_office_worker.vba import generate_vba_macro

BASE = Path('runtime')
UPLOADS = BASE/'uploads'; OUT = BASE/'outputs'
UPLOADS.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
app = FastAPI(title='Skatlaz MCP Office AI Worker', version='2.1.0')

async def _save(upload: UploadFile) -> Path:
    dest = UPLOADS / f'{uuid.uuid4().hex}_{upload.filename}'
    with dest.open('wb') as f:
        shutil.copyfileobj(upload.file, f)
    return dest

@app.get('/')
def root():
    return {'name':'Skatlaz MCP Office AI Worker','version':'2.1.0','tools':['document','sheet','slides','vision','web','security','canvas','sql','vba']}

@app.post('/mcp/document/process')
async def document_process(file: UploadFile = File(...), action: str = Form('summary'), target: str = Form('en')):
    path = await _save(file)
    text = read_document(str(path))
    if action == 'summary': result = summarize_text(text)
    elif action == 'correct': result = correct_text_basic(text)
    elif action == 'translate': result = translate_text_basic(text, target=target)
    else: result = text
    out = OUT / f'{path.stem}_{action}.txt'
    write_txt(str(out), result)
    return {'input': str(path), 'output': str(out), 'result_preview': result[:2000]}

@app.post('/mcp/sheet/process')
async def sheet_process(file: UploadFile = File(...), prompt: str = Form('clean total'), chart: bool = Form(True)):
    path = await _save(file)
    df = clean_table(read_table(str(path)))
    df = apply_prompt_formula(df, prompt)
    summary = None
    try: summary = olap_summary(df).to_dict(orient='records')
    except Exception: summary = []
    chart_path = None
    if chart:
        try: chart_path = create_chart(df, str(OUT/f'{path.stem}_chart.png'), title=f'Gráfico {path.stem}')
        except Exception as e: chart_path = f'chart_error: {e}'
    out_xlsx = save_excel(df, str(OUT/f'{path.stem}_processed.xlsx'), chart_path if chart_path and not str(chart_path).startswith('chart_error') else None)
    return {'output': out_xlsx, 'chart': chart_path, 'summary': summary[:20] if isinstance(summary,list) else summary, 'columns': list(df.columns)}

@app.post('/mcp/slides/create')
def slides_create(title: str = Form('Skatlaz Presentation'), content: str = Form('Slide 1\nSlide 2')):
    sections=[]
    for i, block in enumerate(content.split('\n\n')):
        sections.append({'title': f'{title} {i+1}', 'content': block})
    out = create_presentation(title, sections, str(OUT/f'{uuid.uuid4().hex}_presentation.pptx'))
    return FileResponse(out, filename=Path(out).name)

@app.post('/mcp/vision/read')
async def vision_read(file: UploadFile = File(...)):
    path = await _save(file)
    return {'description': describe_image_basic(str(path)), 'ocr': ocr_image(str(path)), 'codes': read_codes(str(path))}

@app.post('/mcp/qrcode/create')
def qrcode_create(data: str = Form(...)):
    out = create_qrcode(data, str(OUT/f'{uuid.uuid4().hex}_qrcode.png'))
    return FileResponse(out, filename=Path(out).name)

@app.post('/mcp/web/read')
def web_read(url: str = Form(...), products: bool = Form(False)):
    data = read_url(url)
    if products: data['products'] = extract_products_simple(data['text'])
    return data

@app.post('/mcp/security/hash')
async def security_hash(file: UploadFile = File(...)):
    path = await _save(file)
    return {'file': str(path), 'sha256': sha256_file(str(path))}

@app.post('/mcp/security/encrypt')
async def security_encrypt(file: UploadFile = File(...), password: str = Form(...)):
    path = await _save(file)
    out = encrypt_file(str(path), password)
    return FileResponse(out, filename=Path(out).name)

@app.post('/mcp/canvas/report')
def canvas_report(title: str = Form('Relatório Skatlaz'), body: str = Form('Conteúdo do relatório')):
    out = create_report_html(title, body, str(OUT/f'{uuid.uuid4().hex}_report.html'))
    return FileResponse(out, filename=Path(out).name)

@app.post('/mcp/sql/query')
async def sql_query(file: UploadFile = File(...), query: str = Form('select name from sqlite_master where type="table"')):
    path = await _save(file)
    df = sqlite_query(str(path), query)
    return {'columns': list(df.columns), 'rows': df.head(100).to_dict(orient='records')}

@app.post('/mcp/vba/generate')
def vba_generate(prompt: str = Form(...)):
    return {'vba': generate_vba_macro(prompt)}
