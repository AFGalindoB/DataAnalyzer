import numpy as np
import math
import matplotlib.pyplot as plt

def valor_mas_cercano(array, valor):
    idx = np.abs(array - valor).argmin()
    return array[idx]

def regresion_lineal(x, y):
    """Regresión lineal (actualizada para compatibilidad con los nuevos modelos)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    Sxx = sum((xi - mean_x) ** 2 for xi in x)
    Sxy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    Syy = sum((yi - mean_y) ** 2 for yi in y)

    b1 = Sxy / Sxx
    b0 = mean_y - b1 * mean_x

    r = Sxy / math.sqrt(Sxx * Syy)
    r2 = r ** 2
    SST = Syy
    SSR = b1 * Sxy
    SSE = SST - SSR
    s = math.sqrt(SSE / (n - 2)) if n > 2 else 0

    predict = lambda xval: b0 + b1 * xval

    return {
        "b0": b0, "b1": b1,
        "r": r, "r2": r2,
        "s": s,
        "SSR": SSR, "SSE": SSE, "SST": SST,
        "mean_x": mean_x, "mean_y": mean_y, "n": n,
        "model": "lineal",
        "equation": f"Ŷ = {b0:.4f} + {b1:.4f} * X",
        "predict": predict
    }

def graficar_regresion(x, y, resultados):
    """Gráfica generalizada (funciona para todos los modelos)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    model = resultados["model"]
    y_pred = resultados["predict"](x)
    residuos = y - y_pred

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.scatter(x, y, alpha=0.5, label="Datos observados")

    x_min, x_max = x.min(), x.max()
    if model == "logaritmica":
        x_min = max(x_min, 1e-6)
    x_line = np.linspace(x_min, x_max, 200)
    y_line = resultados["predict"](x_line)

    ax1.plot(x_line, y_line, color="red", linewidth=2,
             label=f"Modelo {model.capitalize()}\n{resultados['equation']}")
    ax1.set_title(f"Dispersión y curva de regresión ({model.capitalize()})")
    ax1.set_xlabel("X (variable independiente)")
    ax1.set_ylabel("Y (variable dependiente)")
    ax1.legend()

    ax2.scatter(y_pred, residuos, alpha=0.5, color="steelblue")
    ax2.axhline(0, color="red", linewidth=1.5, linestyle="--")
    ax2.set_title("Gráfico de residuos")
    ax2.set_xlabel("Ŷ (valores ajustados)")
    ax2.set_ylabel("Residuo (Y - Ŷ)")

    plt.tight_layout()
    plt.show()

def filtrar_atipicos(x, y, metodo="iqr", porcentaje=0.05):
    """(Sin cambios - se mantiene igual)"""
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
                 if lim_x[0] <= xi <= lim_x[1] and lim_y[0] <= yi <= lim_y[1]]

    elif metodo == "recorte":
        k = int(len(pares) * porcentaje)
        pares_x = sorted(pares, key=lambda p: p[0])
        pares = pares_x[k: len(pares_x) - k] if k > 0 else pares_x
        pares_y = sorted(pares, key=lambda p: p[1])
        pares = pares_y[k: len(pares_y) - k] if k > 0 else pares_y

    elif metodo == "zscore":
        mean_x, std_x = np.mean(x), np.std(x, ddof=1)
        mean_y, std_y = np.mean(y), np.std(y, ddof=1)
        pares = [(xi, yi) for xi, yi in pares
                 if abs((xi - mean_x) / std_x) <= 3 and abs((yi - mean_y) / std_y) <= 3]

    x_f = np.array([p[0] for p in pares], dtype=float)
    y_f = np.array([p[1] for p in pares], dtype=float)
    n_eliminados = n_original - len(pares)
    return x_f, y_f, n_eliminados

# ==================== NUEVAS REGRESIONES ====================

def regresion_exponencial(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if np.any(y <= 0):
        raise ValueError("Para regresión exponencial todos los valores de Y deben ser > 0.")
    ln_y = np.log(y)
    res = regresion_lineal(x, ln_y)
    a = np.exp(res["b0"])
    b = res["b1"]
    y_pred = a * np.exp(b * x)
    mean_y = np.mean(y)
    SST = np.sum((y - mean_y)**2)
    SSE = np.sum((y - y_pred)**2)
    r2 = 1 - SSE / SST if SST != 0 else 0
    r = np.sign(b) * np.sqrt(r2) if r2 > 0 else 0
    s = np.sqrt(SSE / (len(x) - 2)) if len(x) > 2 else 0
    return {
        "model": "exponencial", "a": a, "b": b,
        "r": r, "r2": r2, "s": s,
        "SSR": SST - SSE, "SSE": SSE, "SST": SST,
        "equation": f"Ŷ = {a:.4f} * e^({b:.4f} * X)",
        "predict": lambda xval: a * np.exp(b * xval)
    }

def regresion_logaritmica(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if np.any(x <= 0):
        raise ValueError("Para regresión logarítmica todos los valores de X deben ser > 0.")
    ln_x = np.log(x)
    res = regresion_lineal(ln_x, y)
    a = res["b0"]
    b = res["b1"]
    y_pred = a + b * np.log(x)
    mean_y = np.mean(y)
    SST = np.sum((y - mean_y)**2)
    SSE = np.sum((y - y_pred)**2)
    r2 = 1 - SSE / SST if SST != 0 else 0
    r = np.sign(b) * np.sqrt(r2) if r2 > 0 else 0
    s = np.sqrt(SSE / (len(x) - 2)) if len(x) > 2 else 0
    return {
        "model": "logaritmica", "a": a, "b": b,
        "r": r, "r2": r2, "s": s,
        "SSR": SST - SSE, "SSE": SSE, "SST": SST,
        "equation": f"Ŷ = {a:.4f} + {b:.4f} * ln(X)",
        "predict": lambda xval: a + b * np.log(xval)
    }

def regresion_polinomica(x, y, grado=2):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) <= grado:
        raise ValueError(f"Se necesitan al menos {grado + 1} puntos para un polinomio de grado {grado}.")
    coeffs = np.polyfit(x, y, grado)
    y_pred = np.polyval(coeffs, x)
    n = len(x)
    mean_y = np.mean(y)
    SST = np.sum((y - mean_y)**2)
    SSE = np.sum((y - y_pred)**2)
    r2 = 1 - SSE / SST if SST != 0 else 0
    r = np.sqrt(r2)
    df = n - grado - 1
    s = np.sqrt(SSE / df) if df > 0 else 0

    # Construcción bonita de la ecuación
    terms = []
    for i, coef in enumerate(coeffs):
        power = grado - i
        if abs(coef) < 1e-8: continue
        if i == 0:
            coef_str = f"{coef:.4f}"
            sign_str = ""
        else:
            sign_str = " + " if coef >= 0 else " - "
            coef_str = f"{abs(coef):.4f}"
        if power == 0:
            term = coef_str
        elif power == 1:
            term = f"{coef_str} * X"
        else:
            term = f"{coef_str} * X^{power}"
        terms.append(sign_str + term if i > 0 else term)
    equation = "Ŷ = " + "".join(terms) if terms else "Ŷ = 0"

    return {
        "model": "polinomica",
        "coeffs": coeffs.tolist(),
        "grado": grado,
        "r": r, "r2": r2, "s": s,
        "SSR": SST - SSE, "SSE": SSE, "SST": SST,
        "equation": equation,
        "predict": lambda xval: np.polyval(coeffs, xval)
    }