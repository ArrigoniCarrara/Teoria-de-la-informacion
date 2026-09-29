import math
import random
from math import log2

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
COD_6 = ["(]", "]", "[)", ")", "(["]           # Ingresa Codigo, ej: ["0", "10", "110", "111"]
LISTAPRO_6 = [0.15, 0.25, 0.05, 0.45, 0.10]       # Probabilidades de cada palabra-codigo, ej: [0.5, 0.25, 0.125, 0.125]
N_MONTECARLO_6 = 5     # cantidad de simbolos a predecir con Monte Carlo (al final)
# ---------------------------------------------------------------------------


def inecuacion_kraft(cod, listaALF):
    r = len(listaALF)
    aux = 0
    for x in cod:
        aux += r ** -len(x)
    return aux


def listas_tipo_codigo(cod, listaALF, listaLong):
    for x in cod:
        listaLong.append(len(x))
        for ch in x:
            if ch not in listaALF:
                listaALF.append(ch)


def nosingular(cod):
    return len(cod) == len(set(cod))


def instantaneo(cod):
    if nosingular(cod):
        for i in range(len(cod)):
            for j in range(len(cod)):
                if i != j:
                    if cod[i].startswith(cod[j]):
                        return False
    else:
        return False
    return True

def univocamente_decodificable(cod): # Solo para verificacion compacto
    if nosingular(cod):
        if instantaneo(cod):
            return True

        C = set(cod)
        S1 = C
        conjuntos_vistos = []
        S_i = S1

        while True:
            S_siguiente = set()

            for x in S1:
                for y in S_i:
                    if x != y:
                        if y.startswith(x):
                            sufijo = y[len(x):]
                            S_siguiente.add(sufijo)
                        elif x.startswith(y):
                            sufijo = x[len(y):]
                            S_siguiente.add(sufijo)

            if not S_siguiente:
                return True

            if S_siguiente & C:
                return False

            if S_siguiente in conjuntos_vistos:
                return True

            conjuntos_vistos.append(S_siguiente)
            S_i = S_siguiente
    return False

def univocamente_decodificable_print(cod): #Imprime sardinas_patterson
    if not nosingular(cod):
        return False

    if instantaneo(cod):
        return True
    
    print("----- Sardinas-Patterson -----")

    C0 = set(cod)
    print(f"S0 = {C0}  (palabras código)")

    conjuntos_vistos = []
    S_anterior = C0   # primera vuelta compara S0 contra sí mismo -> genera S1
    n = 1

    while True:
        S_nuevo = set()

        for x in C0:
            for y in S_anterior:
                if x != y:
                    if y.startswith(x):
                        S_nuevo.add(y[len(x):])
                    elif x.startswith(y):
                        S_nuevo.add(x[len(y):])

        print(f"S{n} = {S_nuevo}")

        # conjunto vacío
        if not S_nuevo:
            print(f"-> S{n} salió vacío. El proceso se cierra sin tocar S0.")
            print("Conclusión: el código ES Unívocamente Decodificable.")
            print("----- Fin Sardinas-Patterson -----")
            return True

        # aparece una palabra de S0
        interseccion = S_nuevo & C0
        if interseccion:
            print(f"-> S{n} contiene {interseccion}, que pertenece a S0.")
            print("Conclusión: el código NO es Unívocamente Decodificable.")
            print("----- Fin Sardinas-Patterson -----")
            return False

        # el conjunto ya había aparecido 
        if S_nuevo in conjuntos_vistos:
            print(f"-> S{n} ya había aparecido en un paso anterior.")
            print("Conclusión: el código ES Unívocamente Decodificable.")
            print("----- Fin Sardinas-Patterson -----")
            return True

        conjuntos_vistos.append(S_nuevo)
        S_anterior = S_nuevo
        n += 1

def long_media(listaPro, listaLong):
    aux = 0
    for i in range(len(listaPro)):
        aux += listaPro[i] * listaLong[i]
    return aux


def entropia_tipo_codigo(lista, listaInfo):
    entropia = 0
    for i, num in enumerate(lista):
        entropia += num * listaInfo[i]
    return entropia


def generar_lista_info_tipo_codigo(lista, listaInfo, listaALF):
    r = len(listaALF)
    for num in lista:
        valor = math.log(1 / num, r)
        listaInfo.append(valor)


def compacto(cod, listaInfo, listaLong):
    if univocamente_decodificable(cod):
        for i in range(len(listaInfo)):
            if math.ceil(listaInfo[i]) < listaLong[i]:
                return False
        return True
    return False


def montecarlo_tipo_codigo(num, cod, listaPro, prediccion):
    listaAcum = []
    ant = 0
    for pro in listaPro:
        listaAcum.append(ant + pro)
        ant = ant + pro

    for i in range(num):
        rand = random.random()
        ant = 0
        n = 0
        for j in listaAcum:
            if ant <= rand < j:
                prediccion.append(cod[n])
                break
            n = n + 1
            ant = j



print("\n--- ANALISIS DE UN CODIGO (Tipo_codigo.py) ---")
cod = COD_6
listaPro = LISTAPRO_6
print(cod)

if not nosingular(cod):
    print("Clasificacion: Codigo Bloque (Singular)")
else:
    if instantaneo(cod):
        print("Clasificacion: Instantaneo")
    else:
        if univocamente_decodificable_print(cod):
            print("Clasificacion: Univocamente Decodificable")
        else:
            print("Clasificacion: No Singular")


listaALF = []
listaLong = []
listas_tipo_codigo(cod, listaALF, listaLong)
print("Lista alfabeto: ", listaALF)
print("Lista Li: ", listaLong)

kraft = inecuacion_kraft(cod, listaALF)
print("Kraft: ", kraft)

listaInfo = []
generar_lista_info_tipo_codigo(listaPro, listaInfo, listaALF)
entropia = entropia_tipo_codigo(listaPro, listaInfo)
print("Entropia de la Fuente: ", entropia)

L_media = long_media(listaPro, listaLong)
print("Longitud media: ", L_media)

if compacto(cod, listaInfo, listaLong):
    print("Es Compacto")
else:
    print("No es Compacto")

prediccion = []
montecarlo_tipo_codigo(N_MONTECARLO_6, cod, listaPro, prediccion)
print("Prediccion Monte Carlo:", prediccion)
    
