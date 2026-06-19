class TXTLoader:
    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
