import requests

class MarketService:
    def stock_quote(self, symbol: str) -> dict:
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            return {"symbol": symbol.upper(), "last_price": float(info.get("last_price") or info.get("lastPrice")), "currency": info.get("currency", ""), "source": "yfinance"}
        except Exception as e:
            return {"symbol": symbol.upper(), "error": str(e), "source": "yfinance"}

    def crypto_quote(self, coin_id: str = "bitcoin", vs_currency: str = "usd") -> dict:
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            data = requests.get(url, params={"ids": coin_id, "vs_currencies": vs_currency}, timeout=12).json()
            return {"coin_id": coin_id, "vs_currency": vs_currency, "price": data.get(coin_id, {}).get(vs_currency), "source": "coingecko"}
        except Exception as e:
            return {"coin_id": coin_id, "error": str(e), "source": "coingecko"}
