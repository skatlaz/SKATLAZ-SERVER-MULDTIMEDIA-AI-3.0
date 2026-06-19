from fastapi import FastAPI
from pydantic import BaseModel
from skatlaz_money_mcp.modules.currency import CurrencyService
from skatlaz_money_mcp.modules.markets import MarketService
from skatlaz_money_mcp.modules.finance import compound_interest, roi, loan_payment
from skatlaz_money_mcp.modules.products import ProductStore
from skatlaz_money_mcp.modules.sheets import analyze as sheet_analyze, chart as sheet_chart, olap_summary
from skatlaz_money_mcp.modules.reports import create_pdf

app = FastAPI(title="Skatlaz Money MCP", version="2.0")
currency = CurrencyService()
market = MarketService()
products = ProductStore()

class ConvertIn(BaseModel):
    amount: float
    base: str
    target: str

class CompoundIn(BaseModel):
    principal: float
    annual_rate: float
    periods: int
    contributions: float = 0.0

class LoanIn(BaseModel):
    principal: float
    annual_rate: float
    months: int

class ProductIn(BaseModel):
    name: str
    category: str = ""
    price: float = 0.0
    rating: float = 0.0
    marketplace: str = "local"
    url: str = ""
    details: str = ""

class SheetAnalyzeIn(BaseModel):
    path: str

class SheetChartIn(BaseModel):
    path: str
    x: str
    y: str
    kind: str = "bar"
    output_name: str = "chart.png"

class OlapIn(BaseModel):
    path: str
    index: str
    values: str
    aggfunc: str = "sum"

class ReportIn(BaseModel):
    title: str
    lines: list[str]
    filename: str = "money_report.pdf"

@app.get("/health")
def health():
    return {"status": "ok", "mcp": "skatlaz_money_mcp", "version": "2.0"}

@app.post("/mcp/money/convert")
def convert(payload: ConvertIn):
    return currency.convert(payload.amount, payload.base, payload.target)

@app.get("/mcp/money/rate/{base}/{target}")
def rate(base: str, target: str):
    return currency.rate(base, target)

@app.get("/mcp/market/stock/{symbol}")
def stock(symbol: str):
    return market.stock_quote(symbol)

@app.get("/mcp/market/crypto/{coin_id}")
def crypto(coin_id: str, vs_currency: str = "usd"):
    return market.crypto_quote(coin_id, vs_currency)

@app.post("/mcp/finance/compound")
def compound(payload: CompoundIn):
    return compound_interest(payload.principal, payload.annual_rate, payload.periods, payload.contributions)

@app.post("/mcp/finance/loan")
def loan(payload: LoanIn):
    return loan_payment(payload.principal, payload.annual_rate, payload.months)

@app.get("/mcp/finance/roi")
def calc_roi(initial: float, final: float):
    return roi(initial, final)

@app.post("/mcp/product/add")
def add_product(payload: ProductIn):
    return products.add(payload.model_dump())

@app.get("/mcp/product/search")
def search_products(query: str = "", category: str = ""):
    return products.search(query or None, category or None)

@app.get("/mcp/product/compare")
def compare_products(query: str = "", category: str = ""):
    return products.compare(products.search(query or None, category or None))

@app.post("/mcp/sheet/analyze")
def sheet_an(payload: SheetAnalyzeIn):
    return sheet_analyze(payload.path)

@app.post("/mcp/sheet/chart")
def sheet_ch(payload: SheetChartIn):
    return {"chart": sheet_chart(payload.path, payload.x, payload.y, payload.kind, payload.output_name)}

@app.post("/mcp/sheet/olap")
def sheet_olap(payload: OlapIn):
    return {"rows": olap_summary(payload.path, payload.index, payload.values, payload.aggfunc)}

@app.post("/mcp/report/pdf")
def report_pdf(payload: ReportIn):
    return {"pdf": create_pdf(payload.title, payload.lines, payload.filename)}
