def extension_fuente(alfabeto, distribucion, N, nuevoAlfabeto, nuevaDistribucion):
    alf = ['']
    pro = [1]
    
    for x in range(N): #cada x++ es un orden
        alfTemp = []
        proTemp = []
        for i in range(len(alfabeto)):
            for j in range(len(alf)):
                alfTemp.append(alfabeto[i] + alf[j])
                proTemp.append(distribucion[i] * pro[j])
        alf = alfTemp
        pro = proTemp

    nuevoAlfabeto.extend(alf)      
    nuevaDistribucion.extend(pro)  



listaAlf = ['x', 'y', 'z'] 
listaPro = [0.5, 0.1, 0.4]
num = 3
nuevoAlf = []
nuevoPro = []
extension_fuente(listaAlf, listaPro, num, nuevoAlf, nuevoPro)
print(nuevoAlf)   
print(nuevoPro)  
