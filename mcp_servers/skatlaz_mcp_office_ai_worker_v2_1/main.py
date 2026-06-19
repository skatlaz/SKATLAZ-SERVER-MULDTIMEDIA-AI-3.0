import sys
from pathlib import Path


def demo():
    from skatlaz_office_worker.canvas import create_report_html
    from skatlaz_office_worker.vision import create_qrcode
    from skatlaz_office_worker.vba import generate_vba_macro
    out = Path('output_files'); out.mkdir(exist_ok=True)
    print('Skatlaz MCP Office AI Worker v2.1 demo')
    print(create_report_html('Demo Skatlaz', 'Relatório gerado com sucesso.', str(out/'demo_report.html')))
    print(create_qrcode('https://skatlaz.com', str(out/'skatlaz_qrcode.png')))
    print(generate_vba_macro('exportar PDF'))


def server():
    import uvicorn
    uvicorn.run('skatlaz_office_worker.api.server:app', host='127.0.0.1', port=8077, reload=False)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        server()
    else:
        demo()
