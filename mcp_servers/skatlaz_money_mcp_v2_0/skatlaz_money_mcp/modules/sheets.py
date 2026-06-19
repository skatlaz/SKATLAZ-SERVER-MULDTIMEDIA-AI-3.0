from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

def read_table(path: str):
    p = Path(path)
    if p.suffix.lower() == ".csv":
        return pd.read_csv(p)
    return pd.read_excel(p)

def analyze(path: str) -> dict:
    df = read_table(path)
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "numeric_summary": df.describe(include="number").fillna(0).to_dict(),
        "missing_values": df.isna().sum().to_dict()
    }

def chart(path: str, x: str, y: str, kind: str = "bar", output_name: str = "chart.png") -> str:
    df = read_table(path)
    ax = df.plot(x=x, y=y, kind=kind)
    ax.set_title(f"{y} por {x}")
    out = OUT / output_name
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return str(out)

def olap_summary(path: str, index: str, values: str, aggfunc: str = "sum") -> dict:
    df = read_table(path)
    table = pd.pivot_table(df, index=index, values=values, aggfunc=aggfunc)
    return table.reset_index().to_dict(orient="records")
