def promedio(lista_numeros):
    suma = sum(lista_numeros)
    cantidad = len(lista_numeros)
    return suma / cantidad

numeros = [1, 2, 3, 4, 5]
print(promedio(numeros))
