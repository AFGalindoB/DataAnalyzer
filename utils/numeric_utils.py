import numpy as np

def valor_mas_cercano(array, valor):
    idx = np.abs(array - valor).argmin()
    return array[idx]