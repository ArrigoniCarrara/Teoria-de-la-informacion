from random import random
def Listasparalelas(cadena, listaAlf, listaPro):

    long = len(cadena)

    for char in cadena:
        if char not in listaAlf:
            listaALF.append(char)
            listaPro.append(cadena.count(char)/long)
        
            
def Montecarlo(num, listaALF, listaPro, prediccion):

    for i in range(num):
        ant = 0;
        for i in range(len(listaPro)):
            aleatorio = random(0, 1)
            if (aleatorio > ant and aleatorio <= ant + listaPro[i]):
                prediccion.append(listaALF[i])
                break
            else:
                ant = ant + listaPro[i];
            


cadena = ['R', 'A', 'D', 'A', 'R']
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