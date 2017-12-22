import numpy as np

'''retorna o vetor normalizado (com norma == 1)'''
def grand_schimidt(vetor_v, vetor_n):
    num = np.dot(vetor_v, vetor_n)
    den = np.dot(vetor_n, vetor_n)
    aux = float(num / den)
    return np.dot(aux, vetor_n)

def normalizar(vetor):
    prod_interno = np.dot(vetor, vetor)
    norma = np.sqrt(prod_interno)
    return vetor / norma

