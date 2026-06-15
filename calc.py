def calculate_erlang_b(A: float, V: int) -> float:
    # A - ruch całkowity - w Erl
    # V - dostępne kanały
    if A <= 0: return 0.0
    block = 1.0
    for i in range(1, V + 1):
        block = 1.0 + (i / A) * block
    return 1.0 / block


def calculate_engset(S: int, V: int, alpha: float) -> float:
    # S - ilość źródeł
    # V - dostępne kanały
    # alpha - natężenie ruchu jednego źródła
    if V >= S: return 0.0
    if alpha <= 0.0: return 0.0

    inv_PB = 1.0
    for i in range(1, V + 1):
        inv_PB = 1.0 + (i / ((S - i) * alpha)) * inv_PB

    return 1.0 / inv_PB
