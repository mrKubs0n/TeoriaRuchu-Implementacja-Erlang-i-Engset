import math


def calculate_erlang_b(A: float, V: int) -> float:
    #iteracyjny odpowiednik
    #A - ruch całkowity - w Erl
    #V - dostępne kanały
    if A <= 0: return 0.0
    block = 1.0
    for i in range(1, V + 1):
        block = 1.0 + (i / A) * block
    return 1.0 / block


def calculate_engset(S: int, V: int, alpha: float) -> float:
    #S - ilość źródeł
    #V - dostępne kanały
    #alpha - natężenie ruchu jednego źródła
    if V >= S: return 0.0
    d = 0.0
    for i in range(V + 1):
        d += math.comb(S - 1, i) * (alpha ** i)
    n = math.comb(S - 1, V) * (alpha ** V)
    return n / d


if __name__ == "__main__":
    print("--- Erlang B  ---")
    print(f"PB:",calculate_erlang_b(5, 2))

    print("--- Engset ---")
    print(f"PB:",calculate_engset(5, 2, 0.5))

