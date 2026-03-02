import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict as dd
import os
import sys
import utils.User_Utils as user_f
import utils.numeric_utils as num_f

class Tabla:
    def __init__(self):
        
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.path_tablas = os.path.join(self.root_path, "tablas")
        
        print("Bienvenido a DataAnalyzer")

        self.setup_configs()

        opciones = {
            "Crear tabla":self.crear_tabla, 
            "Realizar tabla de frecuencias":self.realizar_tabla_de_frecuencias,
            "Realizar grafica de tallos y hojas":self.realizar_grafica_tallos_hojas,
            "Realizar grafica de cajas y bigotes":self.realizar_grafica_cajas_bigotes,
            "Realizar histograma":self.realizar_histograma,
            "Calcular muestra":self.calcular_muestra,
            "Salir":self.salir
        }
        lista_opciones = list(opciones.keys())

        while True:
            opcion_elegida = user_f.select_option(lista_opciones, "\n¿Que desea hacer?:")
            opciones[opcion_elegida]()
    
    def salir(self):
        print("Saliendo del programa...")
        sys.exit()

    def setup_configs(self):
        if not os.path.exists(self.path_tablas):
            os.makedirs(self.path_tablas)
            print("Carpeta 'tablas' creada exitosamente.")
        else:
            print("La carpeta 'tablas' ya existe.")

    def crear_tabla(self):
        datos = []
        contador = 1
        
        nombre_tabla = input("Ingrese el nombre de la tabla (sin extension): ")
        path_tabla = os.path.join(self.path_tablas, f"{nombre_tabla}.csv")

        row = user_f.get_positive_integer("Ingrese el numero de filas: ")
        column = user_f.get_positive_integer("Ingrese el numero de columnas: ")
        tipo = user_f.binary_question("¿Los datos son todos enteros?", "s/n")

        # Ingresar datos con validacion
        for r in range(row):
            fila = []
            for c in range(column):
                while True:
                    try:
                        data = input(f"Ingrese el dato #{contador}:")
                        data = int(data) if tipo else float(data)
                        fila.append(data)
                        contador += 1
                        break
                    except ValueError:
                        print(f"Error. Escriba un valor {'entero' if tipo else 'decimal'}.")
            datos.append(fila)
        
        # Crear tabla y guardarla en CSV
        tabla = pd.DataFrame(datos); print(tabla)
        tabla.to_csv(path_tabla, index=False, header=False)
        print("Archivo CSV guardado correctamente ✔")

    def calcular_muestra(self):
        tabla = user_f.get_table(self.path_tablas)
        tabla = tabla.values.flatten()
        print(tabla, np.sort(tabla), sep="\n\n")

        n = len(tabla)
        print(f"n = {n}")

        media = np.mean(tabla)
        print(f"Media = {media}")

        mediana = np.median(tabla)
        print(f"Mediana = {mediana}")

        moda = pd.Series(tabla).mode().values
        print(f"Moda = {moda}")

        varianza = np.var(tabla, ddof=1)
        print(f"Varianza = {varianza}")

        desviacion_estandar = np.sqrt(varianza)
        print(f"Desviacion Estandar = {desviacion_estandar}")

        cuartiles = np.percentile(tabla, [25, 50, 75], method="weibull")
        print(f"Cuartiles = {cuartiles}")

        rango_intercuartilico = cuartiles[2] - cuartiles[0]
        print(f"Rango Intercuartilico = {rango_intercuartilico}")
    
    def realizar_tabla_de_frecuencias(self):
        tabla = user_f.get_table(self.path_tablas)

        k = user_f.get_positive_integer("Ingrese la cantidad de clases: ")

        # Tomar todos los datos como un array y ordenarlos
        datos = tabla.values.flatten()
        datos_ordenados = np.sort(datos)

        # Min, max reales y valores únicos ordenados
        min_val = datos_ordenados.min()
        max_val = datos_ordenados.max()
        valores_unicos = np.unique(datos_ordenados)

        # Crear límites teóricos para las clases
        bins_teoricos = np.linspace(min_val, max_val, k + 1)

        bins = []
        
        # Para cada límite teórico, encontrar el valor más cercano en los datos únicos
        for b in bins_teoricos[:-1]:  # todos menos el último
            bins.append(num_f.valor_mas_cercano(valores_unicos, b))

        # evitar duplicados por cercanía
        bins = sorted(set(bins))

        # asegurar que el primer límite sea el mínimo real
        bins[0] = min_val

        # última clase hasta infinito
        bins.append(np.inf)

        bins = np.array(bins)

        # Crear clases [a, b)
        clases = pd.cut(
            datos_ordenados,
            bins=bins,
            right=False,
            include_lowest=True
        )

        # Tabla de frecuencias
        tabla_frecuencias = clases.value_counts().sort_index()
        print("\n",datos_ordenados, end="\n\n")
        print(tabla_frecuencias)
        print("Cantidad de clases:", len(tabla_frecuencias))

    def realizar_grafica_tallos_hojas(self):
        tabla = user_f.get_table(self.path_tablas)
        datos = tabla.values.flatten()
        datos = np.sort(datos)
        print(f"Datos: {datos}")

        tipo = user_f.binary_question("¿Los datos son enteros?", "s/n")
        if tipo:
            escala_hoja = user_f.get_positive_integer("Ingrese la escala de la hoja: ")
        else:
            escala_hoja = float(input("Ingrese la escala de la hoja: "))

        tallos = dd(list)

        for valor in datos:
            tallo = valor // escala_hoja
            hoja = valor % escala_hoja
            tallos[tallo].append(hoja)

        print("\nGráfico de Tallo y Hoja:\n")

        for tallo in sorted(tallos.keys()):
            hojas = " ".join(str(h) for h in sorted(tallos[tallo]))
            print(f"{tallo} | {hojas}")

    def realizar_grafica_cajas_bigotes(self):
        tabla = user_f.get_table(self.path_tablas)
        datos = tabla.values.flatten()
        datos = np.sort(datos)

        q1, mediana, q3 = np.percentile(datos, [25, 50, 75], method="weibull")

        iqr = q3 - q1
        limite_inf = q1 - 1.5 * iqr
        limite_sup = q3 + 1.5 * iqr

        print(f"Q1: {q1}")
        print(f"Mediana: {mediana}")
        print(f"Q3: {q3}")
        print(f"IQR: {iqr}")
        print(f"Limite inferior: {limite_inf}")
        print(f"Limite superior: {limite_sup}")

        plt.figure()
        plt.boxplot(datos, vert=True)
        plt.title("Gráfica de Caja y Bigotes")
        plt.show()
    
    def realizar_histograma(self):
        tabla = user_f.get_table(self.path_tablas)
        datos = tabla.values.flatten()
        datos = np.sort(datos)

        print(f"Datos:\n{datos}\n")

        # Preguntar cantidad de clases (bins)
        k = user_f.get_positive_integer("Ingrese la cantidad de clases (bins): ")

        # Estadísticos básicos
        media = np.mean(datos)
        mediana = np.median(datos)

        print(f"Media: {media}")
        print(f"Mediana: {mediana}")
        print(f"Min: {datos.min()}")
        print(f"Max: {datos.max()}")

        # Crear histograma
        plt.figure()
        plt.hist(datos, bins=k)
        plt.axvline(media)
        plt.axvline(mediana)

        plt.title("Histograma")
        plt.xlabel("Valores")
        plt.ylabel("Frecuencia")

        plt.show()

if __name__ == "__main__":
    x = Tabla()