# Skatlaz Money MCP v2.0

MCP financeiro para o Skatlaz Server AI 2.0.

## Recursos

- Conversão de moedas via APIs gratuitas/open source com fallback local
- Taxas de câmbio
- Bolsa de valores via yfinance
- Criptomoedas via CoinGecko public API
- Cálculos de juros compostos, ROI, parcelas e projeções
- Análise de planilhas CSV/XLSX com pandas
- Geração de gráficos PNG
- Produtos/e-commerce via JSON/CSV local
- Comparação de produtos por preço/rating
- Relatórios PDF simples
- API FastAPI estilo MCP
- CLI de teste

## Instalação Windows

```bat
install_windows.bat
```

## Rodar servidor

```bat
run_server.bat
```

Acesse:

```text
http://127.0.0.1:8020/docs
```

## Teste CLI

```bat
python main.py demo
python main.py convert 100 USD BRL
python main.py stock MSFT
python main.py crypto bitcoin
```

## Endpoints principais

- `GET /health`
- `POST /mcp/money/convert`
- `GET /mcp/money/rate/{base}/{target}`
- `GET /mcp/market/stock/{symbol}`
- `GET /mcp/market/crypto/{coin_id}`
- `POST /mcp/finance/compound`
- `POST /mcp/sheet/analyze`
- `POST /mcp/product/add`
- `GET /mcp/product/search`
- `POST /mcp/report/pdf`

