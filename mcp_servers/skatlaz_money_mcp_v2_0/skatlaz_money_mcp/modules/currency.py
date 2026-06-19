import json
from pathlib import Path
import requests

DATA = Path(__file__).resolve().parents[1] / "data"
FALLBACK = DATA / "currency_fallback.json"

DEFAULT_RATES = {
    "base": "USD",
    "rates": {
        "USD": 1.0,
        "BRL": 5.20,
        "EUR": 0.92,
        "GBP": 0.78,
        "JPY": 155.0,
        "CAD": 1.36,
        "AUD": 1.50,
        "CHF": 0.90,
        "CNY": 7.24,
        "ARS": 900.0,
        "MXN": 17.0
    }
}

class CurrencyService:
    def __init__(self):
        DATA.mkdir(parents=True, exist_ok=True)
        if not FALLBACK.exists():
            FALLBACK.write_text(json.dumps(DEFAULT_RATES, indent=2), encoding="utf-8")

    def _fallback_rates(self):
        return json.loads(FALLBACK.read_text(encoding="utf-8"))["rates"]

    def rate(self, base: str, target: str) -> dict:
        base = base.upper()
        target = target.upper()
        try:
            url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
            data = requests.get(url, timeout=12).json()
            if "rates" in data and target in data["rates"]:
                return {"base": base, "target": target, "rate": float(data["rates"][target]), "source": "frankfurter"}
        except Exception:
            pass
        rates = self._fallback_rates()
        if base not in rates or target not in rates:
            raise ValueError(f"Moeda não encontrada no fallback: {base}/{target}")
        rate = rates[target] / rates[base]
        return {"base": base, "target": target, "rate": rate, "source": "local_fallback"}

    def convert(self, amount: float, base: str, target: str) -> dict:
        r = self.rate(base, target)
        return {"amount": amount, "base": base.upper(), "target": target.upper(), "rate": r["rate"], "result": amount * r["rate"], "source": r["source"]}
