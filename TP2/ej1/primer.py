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
    


lista = [0.2, 0.7, 0.1]
listaInfo = []
Generolista(lista, listaInfo)
print(lista)
print(listaInfo)
print("Entropia = ", Entropia(lista, listaInfo))