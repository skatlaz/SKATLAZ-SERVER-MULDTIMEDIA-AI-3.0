import argparse
from skatlaz_money_mcp.modules.currency import CurrencyService
from skatlaz_money_mcp.modules.markets import MarketService
from skatlaz_money_mcp.modules.finance import compound_interest
from skatlaz_money_mcp.modules.products import ProductStore


def main():
    parser = argparse.ArgumentParser(description="Skatlaz Money MCP CLI")
    sub = parser.add_subparsers(dest="cmd")

    c = sub.add_parser("convert")
    c.add_argument("amount", type=float)
    c.add_argument("base")
    c.add_argument("target")

    r = sub.add_parser("rate")
    r.add_argument("base")
    r.add_argument("target")

    s = sub.add_parser("stock")
    s.add_argument("symbol")

    cr = sub.add_parser("crypto")
    cr.add_argument("coin_id")

    demo = sub.add_parser("demo")

    args = parser.parse_args()
    cur = CurrencyService()
    market = MarketService()

    if args.cmd == "convert":
        print(cur.convert(args.amount, args.base, args.target))
    elif args.cmd == "rate":
        print(cur.rate(args.base, args.target))
    elif args.cmd == "stock":
        print(market.stock_quote(args.symbol))
    elif args.cmd == "crypto":
        print(market.crypto_quote(args.coin_id))
    elif args.cmd == "demo":
        print("Compound:", compound_interest(1000, 0.05, 12))
        print("USD/BRL:", cur.convert(100, "USD", "BRL"))
        store = ProductStore()
        store.add({"name": "Notebook Demo", "category": "informatica", "price": 2500, "rating": 4.5})
        print(store.search("notebook"))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
