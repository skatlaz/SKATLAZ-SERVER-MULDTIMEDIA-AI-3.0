# Skatlaz SurfTask MCP v1.0

MCP para Web & Automação do Skatlaz Server AI 2.0.

## Recursos

- Acessa sites por URL
- Extrai `title`, descrição, metatags, headings, links e imagens
- Cria resumo offline simples da página
- Gera miniatura/screenshot PNG do site com Playwright/Chromium
- Exporta relatório DOCX, CSV e XLSX
- OCR de imagens com Tesseract
- Leitura de QR Code e código de barras
- Geração de QR Code
- API FastAPI estilo MCP
- CLI para testes

## Instalação no Windows

```bat
install_windows.bat
```

O screenshot usa Playwright. O instalador executa:

```bat
python -m playwright install chromium
```

Para OCR, instale o Tesseract OCR no Windows e deixe no PATH.

## Rodar servidor

```bat
run_server.bat
```

API:

- http://127.0.0.1:8787/docs

## Teste CLI

```bat
run_cli.bat https://skatlaz.com --screenshot --docx
```

## Endpoints MCP

```text
POST /mcp/web/analyze
POST /mcp/web/batch
GET  /mcp/web/screenshot?url=https://site.com
POST /mcp/ocr/image
POST /mcp/barcode/read
POST /mcp/qrcode/create
```

## Exemplo de prompt

```text
Acesse https://skatlaz.com, leia as metatags, faça um resumo e crie uma miniatura do site.
```

## Próximas versões

- scraping com regras por domínio
- extração de produtos/preços
- agendamento de tarefas
- envio de e-mails autenticado via painel
- integração com Skatlaz Server AI Agents
- integração com Office Worker para relatórios completos
