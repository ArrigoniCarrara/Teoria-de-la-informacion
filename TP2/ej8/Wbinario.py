from Entropia import Entropia
from Entropia import Generolista

print("Escriba el valor w")
w = float(input())
listaPro = [w, 1 - w]
listaInfo = []
Generolista(listaPro, listaInfo)
print(listaPro)
print(listaInfo)
print("La entropia es = ", Entropia(listaPro, listaInfo))
