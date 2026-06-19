# Skatlaz MCP Office AI Worker v2.1

MCP funcional para o Skatlaz Server AI trabalhar com documentos, planilhas, slides, imagens, OCR, QR/barcode, web, tradução básica, SQL, VBA, segurança e canvas HTML.

## Instalação Windows

```bat
py -3.11 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

OCR opcional: instale o Tesseract e adicione ao PATH.

## Rodar API MCP

```bat
python main.py server
```

Acesse:

```text
http://127.0.0.1:8077/docs
```

## Rodar exemplos

```bat
python main.py demo
```

## Estrutura

- `skatlaz_office_worker/documents`: DOCX, PDF, TXT, HTML, MD, ODT
- `spreadsheets`: XLSX/CSV, fórmulas, gráficos, resumo OLAP simples
- `slides`: criação PPTX
- `vision`: OCR, QR Code, código de barras, descrição básica de imagem
- `web`: leitura de URL, extração de texto, produtos simples
- `security`: criptografia, SHA256, remoção simples de metadados
- `canvas`: HTML/CSS por template, export HTML
- `translator`: tradução básica offline por dicionário + interface para LLM futura
- `sql`: SQLite query/report
- `vba`: gera macros VBA por templates
- `api`: FastAPI estilo MCP

## Observação

A tradução inclusa é básica/offline para testes. Para qualidade profissional, plugue Ollama, DeepSeek, Gemini ou OpenAI no módulo `translator/providers.py`.
