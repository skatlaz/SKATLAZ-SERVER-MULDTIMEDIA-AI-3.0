def compound_interest(principal: float, annual_rate: float, periods: int, contributions: float = 0.0) -> dict:
    value = principal
    history = []
    for i in range(1, periods + 1):
        value = value * (1 + annual_rate) + contributions
        history.append({"period": i, "value": round(value, 2)})
    return {"principal": principal, "annual_rate": annual_rate, "periods": periods, "contributions": contributions, "final_value": round(value, 2), "history": history}

def roi(initial: float, final: float) -> dict:
    if initial == 0:
        raise ValueError("initial não pode ser zero")
    return {"initial": initial, "final": final, "roi_percent": ((final - initial) / initial) * 100}

def loan_payment(principal: float, annual_rate: float, months: int) -> dict:
    monthly = annual_rate / 12
    if monthly == 0:
        payment = principal / months
    else:
        payment = principal * (monthly * (1 + monthly) ** months) / ((1 + monthly) ** months - 1)
    return {"principal": principal, "annual_rate": annual_rate, "months": months, "monthly_payment": round(payment, 2), "total": round(payment * months, 2)}
