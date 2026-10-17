from math import log2

def listas_paralelas(cadena, listaALF, listaPro):
    long = len(cadena)

    for char in cadena:
        if char not in listaALF:
            listaALF.append(char)
            listaPro.append(cadena.count(char) / long)

    parejas_ordenadas = sorted(zip(listaALF, listaPro), key=lambda x: ord(x[0])) # Ordeno los eventos para mayor comodidad (en el orden que corresponda)

    listaALF.clear()
    listaPro.clear()

    for char, pro in parejas_ordenadas:
        listaALF.append(char)
        listaPro.append(pro)

# Es libre de prefijo y muy cercano al óptimo, pero no siempre es óptimo. 
# Como el corte se decide mirando solo la suma de cada mitad, a veces queda una división poco favorable.
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
    h = -sum(p * log2(p) for p in probs)                  # entropía
    l = sum(p * len(c) for p, c in zip(probs, codigos))   # longitud media
    n = h / l                                           # eficiencia
    return h, l, n, 1 - n                             # redundancia = 1 - eta


if __name__ == "__main__":
    cadena = "58784784525368669895745123656253698989656452121702300223659"
    listaALF = []
    pro = []
    listas_paralelas(cadena, listaALF, pro)
    codigo = shannon_fano(pro)

    print(f"{'Símbolo':<8} {'Prob.':<10} Código") #Imprime SIMBOLO PROBABILIDAD CODIGO
    for s, p, c in zip(listaALF, pro, codigo):
        print(f"{s:<8} {p:<10.4f} {c}")

    h, l, n, r = metricas(pro, codigo)
    print(f"H(S) = {h} bits")
    print(f"L = {l} bits")
    print(f"η = {n}")
    print(f"R = {r}")