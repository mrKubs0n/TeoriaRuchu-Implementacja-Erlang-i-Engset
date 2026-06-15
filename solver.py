from calc import calculate_erlang_b, calculate_engset


def solve_erlang_b(A=None, V=None, PB=None, tol=1e-6):
    params = [A, V, PB]
    if params.count(None) != 1:
        raise ValueError("Podaj dokładnie dwie zmienne. Jedna musi być równa None.")

    # blokada
    if PB is None:
        return calculate_erlang_b(A, V)

    # minimalna blokada
    if V is None:
        v = 1
        while calculate_erlang_b(A, v) > PB:
            v += 1
        return v

    # ruch A
    if A is None:
        if PB <= 0.0: return 0.0
        if PB >= 1.0: return float('inf')

        low = 0.0
        high = 1.0

        while calculate_erlang_b(high, V) < PB:
            high *= 2.0

        while high - low > tol:
            mid = (low + high) / 2.0
            if calculate_erlang_b(mid, V) < PB:
                low = mid
            else:
                high = mid
        return (low + high) / 2.0


def solve_engset(S=None, V=None, alpha=None, PB=None, tol=1e-6):
    params = [S, V, alpha, PB]
    if params.count(None) != 1:
        raise ValueError("Podaj dokładnie trzy zmienne. Jedna musi być równa None.")

    # blokada
    if PB is None:
        return calculate_engset(S, V, alpha)

    # liczba kanałów
    if V is None:
        v = 1
        while v < S and calculate_engset(S, v, alpha) > PB:
            v += 1
        return v

    # liczba źródeł
    if S is None:
        s = V + 1
        while calculate_engset(s, V, alpha) <= PB:
            s += 1
        return s - 1

    # alpha
    if alpha is None:
        if PB <= 0.0: return 0.0
        if PB >= 1.0: return float('inf')

        if V >= S:
            raise ValueError(f"Dla S={S} i V={V} prawdopodobieństwo blokady wynosi 0. Nie da się osiągnąć PB={PB}")

        low = 0.0
        high = 1.0
        max_iters = 1000
        iters = 0
        while calculate_engset(S, V, high) < PB:
            high *= 2.0
            iters += 1
            if iters > max_iters:
                raise ValueError("Przekroczono limit iteracji. Wynik dąży do nieskończoności.")

        while high - low > tol:
            mid = (low + high) / 2.0
            if calculate_engset(S, V, mid) < PB:
                low = mid
            else:
                high = mid
        return (low + high) / 2.0
