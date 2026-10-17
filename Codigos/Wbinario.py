from Entropia import Entropia
from Entropia import Generolista
from Secuencia import extension_fuente

print("Escriba el valor w")
w = 0.8
listaPro = [w, 1 - w]
alfabeto = []
alfabeto = ['1', '0']
listaInfo = []
Generolista(listaPro, listaInfo)
print(listaPro)
print(listaInfo)
print("La entropia es = ", Entropia(listaPro, listaInfo))
nuevoalf = []
nuevapro = []
extension_fuente(alfabeto, listaPro, 3, nuevoalf, nuevapro)
print(nuevoalf)
print(nuevapro)