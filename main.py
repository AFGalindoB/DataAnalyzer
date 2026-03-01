import pandas as pd
import numpy as np
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

        # Obtener numero de filas y columnas con validacion
        while True:
            try:
                row = int(input("Ingrese el numero de filas: "))
                column = int(input("Ingrese el numero de columnas: "))
                break
            except ValueError:
                print("Error. Escriba un valor entero")

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

        # Obtener cantidad de clases con validacion
        while True:
            try:
                k = int(input("Ingrese la cantidad de clases: "))
                if k > 0:
                    break
                else:
                    print("Error. Ingrese un numero entero positivo.")
            except ValueError:
                print("Error. Ingrese un valor entero.")

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


if __name__ == "__main__":
    x = Tabla()