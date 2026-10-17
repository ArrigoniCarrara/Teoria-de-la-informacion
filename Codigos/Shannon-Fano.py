from math import log2


def shannon_fano(probs):
    items = [[p, ""] for p in probs]
    if len(items) == 1:
        return ["0"]
    # Se ordena de mayor a menor probabilidad
    codificar(sorted(items, key=lambda x: x[0], reverse=True))
    return [code for _, code in items]


def codificar(items):
    # Caso base: un solo símbolo, ya no hay nada que dividir
    if len(items) <= 1:
        return

    # Se busca el corte que deja las dos mitades con sumas lo más parecidas posible
    total = sum(p for p, _ in items)
    acumulado = 0
    mejor_corte = 1
    mejor_dif = float("inf")
    for i in range(1, len(items)):
        acumulado += items[i - 1][0]
        dif = abs(acumulado - (total - acumulado))
        if dif < mejor_dif:
            mejor_dif = dif
            mejor_corte = i

    arriba = items[:mejor_corte]
    abajo = items[mejor_corte:]

    # Se asigna un bit a cada grupo (igual que el PDF: 1 arriba, 0 abajo)
    for item in arriba:
        item[1] += "1"
    for item in abajo:
        item[1] += "0"

    # Se repite el proceso dentro de cada grupo
    codificar(arriba)
    codificar(abajo)


def metricas(probs, codigos):
    H = -sum(p * log2(p) for p in probs)                  # entropía
    L = sum(p * len(c) for p, c in zip(probs, codigos))   # longitud media
    eta = H / L                                           # eficiencia
    return H, L, eta, 1 - eta                             # redundancia = 1 - eta


if __name__ == "__main__":
    pro = [0.20, 0.27, 0.40, 0.13]
    codigos = shannon_fano(pro)
    for p, c in zip(pro, codigos):
        print(f"{p:.2f} -> {c}")

    H, L, eta, R = metricas(pro, codigos)
    print(f"H(S) = {H:.2f} bits")
    print(f"L = {L:.2f} bits")
    print(f"η = {eta:.4f}")
    print(f"R = {R:.4f}")