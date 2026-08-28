from random import random

def Listasparalelas(cadena, listaAlf, listaPro):

    long = len(cadena)

    for char in cadena:
        if char not in listaAlf:
            listaALF.append(char)
            listaPro.append(cadena.count(char)/long)
        
            
def Montecarlo(num, listaALF, listaPro, prediccion):

    listaAcum = []
    ant = 0;
    for pro in listaPro:
        listaAcum.append(ant + pro)
        ant = ant + pro;

    for i in range(num):
        rand = random()
        ant = 0
        n = 0
        for j in listaAcum:
            if ant <= rand and rand < j:
                prediccion.append(listaALF[n])
                break
            n = n + 1
            ant = j


cadena = "ABDAACAABACADAABDAADABDAAABDCDCDCDC"
listaALF = []
listaPro = []
prediccion = []
num = 5;
Listasparalelas(cadena, listaALF, listaPro)
Montecarlo(num, listaALF, listaPro, prediccion)
print(cadena)
print(listaALF)
print(listaPro)
print(prediccion)