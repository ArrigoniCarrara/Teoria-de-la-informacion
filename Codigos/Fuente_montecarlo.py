from random import random

def Listasparalelas(cadena, listaALF, listaPro):

    long = len(cadena)

    for char in cadena:
        if char not in listaALF:
            listaALF.append(char)
            listaPro.append(cadena.count(char)/long)

    # Ordenar ambos vectores en paralelo según el código ASCII de los caracteres
    # zip() junta (carácter, probabilidad), sorted() ordena por el carácter (ASCII)
    parejas_ordenadas = sorted(zip(listaALF, listaPro), key=lambda x: ord(x[0]))

    # Limpiar y rellenar las listas originales para mantener la modificación por referencia
    listaALF.clear()
    listaPro.clear()
    
    for char, pro in parejas_ordenadas:
        listaALF.append(char)
        listaPro.append(pro)
        
            
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

if __name__ == "__main__":
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