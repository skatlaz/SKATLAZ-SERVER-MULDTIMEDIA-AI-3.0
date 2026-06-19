import json
from pathlib import Path
from typing import Optional

DATA = Path(__file__).resolve().parents[1] / "data"
PRODUCTS = DATA / "products.json"

class ProductStore:
    def __init__(self):
        DATA.mkdir(parents=True, exist_ok=True)
        if not PRODUCTS.exists():
            PRODUCTS.write_text("[]", encoding="utf-8")

    def all(self):
        return json.loads(PRODUCTS.read_text(encoding="utf-8"))

    def save(self, data):
        PRODUCTS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def add(self, product: dict):
        data = self.all()
        product.setdefault("id", len(data) + 1)
        data.append(product)
        self.save(data)
        return product

    def search(self, query: Optional[str] = None, category: Optional[str] = None):
        data = self.all()
        out = []
        q = (query or "").lower()
        c = (category or "").lower()
        for p in data:
            hay = " ".join(str(v) for v in p.values()).lower()
            if q and q not in hay:
                continue
            if c and c not in str(p.get("category", "")).lower():
                continue
            out.append(p)
        return out

    def compare(self, products):
        return sorted(products, key=lambda p: (float(p.get("price", 0)), -float(p.get("rating", 0))))
