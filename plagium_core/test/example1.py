def calcular_promedio(valores):
    total = 0
    for valor in valores:
        total += valor
    return total / len(valores)

mis_numeros = [1, 2, 3, 4, 5]

print(calcular_promedio(mis_numeros))
