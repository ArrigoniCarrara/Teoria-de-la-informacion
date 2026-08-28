from math import log2 
import random

def Entropia(lista, listaInfo):

    i = 0
    entropia = 0
    for num in lista:
        entropia += num * listaInfo[i]
        i = i + 1
    return entropia

def Generolista (lista, listaInfo):

    for num in lista:
         listaInfo.append(log2(1/num))
    

lista = [0.125, 0.025, 0.1, 0.025, 0.005000000000000001, 0.020000000000000004, 0.1, 0.020000000000000004, 0.08000000000000002, 0.025, 0.005000000000000001, 0.020000000000000004, 0.005000000000000001, 0.0010000000000000002, 0.004000000000000001, 0.020000000000000004, 0.004000000000000001, 0.016000000000000004, 0.1, 0.020000000000000004, 0.08000000000000002, 0.020000000000000004, 0.004000000000000001, 0.016000000000000004, 0.08000000000000002, 0.016000000000000004, 0.06400000000000002]
listaInfo = []
Generolista(lista, listaInfo)
print(lista)
print(listaInfo)
print("Entropia = ", Entropia(lista, listaInfo))