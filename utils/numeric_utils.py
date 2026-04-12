import numpy as np
import math
import matplotlib.pyplot as plt

def valor_mas_cercano(array, valor):
    idx = np.abs(array - valor).argmin()
    return array[idx]

def regresion_lineal(x, y):
    """Calcula la regresión lineal simple entre X e Y.
    Retorna un dict con b0, b1, r, r2, s, SSR, SSE, SST."""

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    Sxx = sum((xi - mean_x) ** 2 for xi in x)
    Sxy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    Syy = sum((yi - mean_y) ** 2 for yi in y)

    b1 = Sxy / Sxx
    b0 = mean_y - b1 * mean_x

    r  = Sxy / math.sqrt(Sxx * Syy)
    r2 = r ** 2

    SST = Syy
    SSR = b1 * Sxy
    SSE = SST - SSR
    s   = math.sqrt(SSE / (n - 2))

    return {
        "b0": b0, "b1": b1,
        "r": r,   "r2": r2,
        "s": s,
        "SSR": SSR, "SSE": SSE, "SST": SST,
        "mean_x": mean_x, "mean_y": mean_y,
        "n": n
    }


def graficar_regresion(x, y, resultados):
    """Muestra el diagrama de dispersión con la recta de regresión
    y el gráfico de residuos."""

    b0 = resultados['b0']
    b1 = resultados['b1']

    x_line = [min(x), max(x)]
    y_line = [b0 + b1 * xi for xi in x_line]
    residuos = [yi - (b0 + b1 * xi) for xi, yi in zip(x, y)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Dispersión + recta
    ax1.scatter(x, y, alpha=0.5, label="Datos observados")
    ax1.plot(x_line, y_line, color="red", linewidth=2,
             label=f"Ŷ = {b0:.2f} + {b1:.2f}·X")
    ax1.set_title("Dispersión y recta de regresión")
    ax1.set_xlabel("X (variable independiente)")
    ax1.set_ylabel("Y (variable dependiente)")
    ax1.legend()

    # Residuos
    y_pred = [b0 + b1 * xi for xi in x]
    ax2.scatter(y_pred, residuos, alpha=0.5, color="steelblue")
    ax2.axhline(0, color="red", linewidth=1.5, linestyle="--")
    ax2.set_title("Gráfico de residuos")
    ax2.set_xlabel("Ŷ (valores ajustados)")
    ax2.set_ylabel("Residuo (Y - Ŷ)")

    plt.tight_layout()
    plt.show()

def filtrar_atipicos(x, y, metodo="iqr", porcentaje=0.05):
    """
    Filtra datos atípicos de los pares (x, y) según el método elegido.
    
    Métodos:
      - 'iqr'      : Elimina pares donde X o Y estén fuera de Q1-1.5*IQR / Q3+1.5*IQR
      - 'recorte'  : Elimina el porcentaje inferior y superior (media recortada)
      - 'zscore'   : Elimina pares donde X o Y tengan |z| > 3
    
    :param x: array de valores X
    :param y: array de valores Y
    :param metodo: 'iqr', 'recorte' o 'zscore'
    :param porcentaje: fracción a recortar en cada extremo (solo para 'recorte'), ej: 0.05 = 5%
    :return: (x_filtrado, y_filtrado, n_eliminados)
    """
    import numpy as np
    pares = list(zip(x, y))
    n_original = len(pares)

    if metodo == "iqr":
        def limites_iqr(valores):
            q1, q3 = np.percentile(valores, [25, 75], method="weibull")
            iqr = q3 - q1
            return q1 - 1.5 * iqr, q3 + 1.5 * iqr

        lim_x = limites_iqr(x)
        lim_y = limites_iqr(y)
        pares = [(xi, yi) for xi, yi in pares
                 if lim_x[0] <= xi <= lim_x[1]
                 and lim_y[0] <= yi <= lim_y[1]]

    elif metodo == "recorte":
        k = int(len(pares) * porcentaje)
        # Recortar por X
        pares_x = sorted(pares, key=lambda p: p[0])
        pares = pares_x[k: len(pares_x) - k] if k > 0 else pares_x
        # Recortar por Y
        pares_y = sorted(pares, key=lambda p: p[1])
        pares = pares_y[k: len(pares_y) - k] if k > 0 else pares_y

    elif metodo == "zscore":
        mean_x, std_x = np.mean(x), np.std(x, ddof=1)
        mean_y, std_y = np.mean(y), np.std(y, ddof=1)
        pares = [(xi, yi) for xi, yi in pares
                 if abs((xi - mean_x) / std_x) <= 3
                 and abs((yi - mean_y) / std_y) <= 3]

    x_f = np.array([p[0] for p in pares], dtype=float)
    y_f = np.array([p[1] for p in pares], dtype=float)
    n_eliminados = n_original - len(pares)

    return x_f, y_f, n_eliminados