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
        self.tabla_cargada = None
        
        print("Bienvenido a DataAnalyzer")

        self.setup_configs()

        opciones = {
            "Crear tabla":self.crear_tabla, 
            "Agregar tabla desde archivo":self.agregar_tabla,
            "Cargar_tabla": self.cargar_tabla,
            "Calcular muestra":self.calcular_muestra,
            "Realizar tabla de frecuencias":self.realizar_tabla_de_frecuencias,
            "Realizar grafica de tallos y hojas":self.realizar_grafica_tallos_hojas,
            "Realizar grafica de cajas y bigotes":self.realizar_grafica_cajas_bigotes,
            "Realizar histograma":self.realizar_histograma,
            "Realizar regresión": self.realizar_regresion,
            "Salir":self.salir
        }
        lista_opciones = list(opciones.keys())

        while True:
            opcion_elegida = user_f.select_option(lista_opciones, "\n¿Que desea hacer?:")
            opciones[opcion_elegida]()
    
    def cargar_tabla(self):
        self.tabla_cargada = user_f.seleccionar_tabla(self.path_tablas)

    def _obtener_datos_tabla(self, preguntar_encabezados=True):
        if self.tabla_cargada is None:
            self.cargar_tabla()

        if preguntar_encabezados:
            return user_f.obtener_datos_tabla(self.tabla_cargada)

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

    def agregar_tabla(self):
        print("\nAbriendo explorador de archivos...")
        ruta_origen = user_f.open_file_dialog()
 
        if not ruta_origen:
            print("No se seleccionó ningún archivo.")
            return
 
        if not ruta_origen.lower().endswith(".csv"):
            print("Error: solo se admiten archivos .csv")
            return
 
        nombre_sugerido = os.path.splitext(os.path.basename(ruta_origen))[0]
        nombre = input(f"Nombre para guardar la tabla (Enter para usar '{nombre_sugerido}'): ").strip()
        if not nombre:
            nombre = nombre_sugerido
 
        destino = os.path.join(self.path_tablas, f"{nombre}.csv")
 
        if os.path.exists(destino):
            sobrescribir = user_f.binary_question(
                f"Ya existe '{nombre}.csv'. ¿Desea sobreescribirlo?", "s/n"
            )
            if not sobrescribir:
                print("Operación cancelada.")
                return
 
        import shutil
        shutil.copy2(ruta_origen, destino)
        print(f"Tabla guardada como '{nombre}.csv' ✔")
 
        vista_previa = user_f.binary_question("¿Desea ver una vista previa de los datos?", "s/n")
        if vista_previa:
            df = pd.read_csv(destino, header=None)
            print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            print(df.head(10).to_string(index=False, header=False))

    def calcular_muestra(self):
        tabla = self._obtener_datos_tabla()
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
        tabla = self._obtener_datos_tabla()

        k = user_f.get_positive_integer("Ingrese la cantidad de clases: ")

        datos_ordenados = np.sort(tabla)

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
        tabla = self._obtener_datos_tabla()
        datos = np.sort(tabla)
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
        tabla = self._obtener_datos_tabla()
        datos = np.sort(tabla)

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
        tabla = self._obtener_datos_tabla()
        datos = np.sort(tabla)

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

    def realizar_regresion(self):
        print("\n--- Regresión ---")
        tipos_regresion = {
            "Lineal (Y = β₀ + β₁X)": "lineal",
            "Exponencial (Y = a * e^(bX))": "exponencial",
            "Logarítmica (Y = a + b * ln(X))": "logaritmica",
            "Polinómica": "polinomica"
        }
        lista_tipos = list(tipos_regresion.keys())
        eleccion = user_f.select_option(lista_tipos, "\nSeleccione el tipo de regresión:")
        model_type = tipos_regresion[eleccion]
        self._obtener_datos_tabla(preguntar_encabezados=False)
        tabla = self.tabla_cargada

        print(f"\n--- Regresión {eleccion.split(' (')[0]} ---")
        print("Seleccione la tabla con la variable X (independiente):")
        x = self._obtener_datos_tabla(tabla)

        print("\nSeleccione la tabla con la variable Y (dependiente):")
        y = self._obtener_datos_tabla(tabla)

        if len(x) != len(y):
            print(f"Error: X tiene {len(x)} datos e Y tiene {len(y)}. Deben ser iguales.")
            return

        filtrar = user_f.binary_question("\n¿Desea filtrar datos atípicos antes de la regresión?", "s/n")
        if filtrar:
            metodos = ["IQR (bigotes)", "Recorte por porcentaje", "Z-score (|z| > 3)"]
            keys = ["iqr", "recorte", "zscore"]
            eleccion_f = user_f.select_option(metodos, "Seleccione el método de filtrado:")
            metodo = keys[metodos.index(eleccion_f)]
            porcentaje = 0.05
            if metodo == "recorte":
                while True:
                    try:
                        porcentaje = float(input("Porcentaje a recortar en cada extremo (ej: 5 para 5%): ")) / 100
                        if 0 < porcentaje < 0.5:
                            break
                        print("Ingrese un valor entre 1 y 49.")
                    except ValueError:
                        print("Error. Ingrese un número válido.")
            x, y, eliminados = num_f.filtrar_atipicos(x, y, metodo=metodo, porcentaje=porcentaje)
            print(f"\n  Datos originales : {len(x) + eliminados}")
            print(f"  Datos eliminados : {eliminados}")
            print(f"  Datos restantes  : {len(x)}")

        try:
            if model_type == "lineal":
                resultados = num_f.regresion_lineal(x, y)
            elif model_type == "exponencial":
                resultados = num_f.regresion_exponencial(x, y)
            elif model_type == "logaritmica":
                resultados = num_f.regresion_logaritmica(x, y)
            elif model_type == "polinomica":
                grado = user_f.get_positive_integer("Ingrese el grado del polinomio (1-5 recomendado): ")
                if grado < 1:
                    grado = 1
                if grado > 10:
                    grado = 5
                    print("Grado limitado a 5.")
                resultados = num_f.regresion_polinomica(x, y, grado)
        except ValueError as e:
            print(f"\nError: {e}")
            print("No se pudo calcular la regresión (verifica valores positivos para exp/log).")
            return
        except Exception as e:
            print(f"\nError inesperado: {e}")
            return

        # Resultados
        print("\n========== RESULTADOS ==========")
        print(f"Modelo:             {resultados['model'].capitalize()}")
        print(f"Ecuación:           {resultados['equation']}")
        if resultados['model'] == "lineal":
            print(f"Intercepto (β₀):    {resultados['b0']:.4f}")
            print(f"Pendiente (β₁):     {resultados['b1']:.4f}")
        elif resultados['model'] in ["exponencial", "logaritmica"]:
            print(f"a:                  {resultados['a']:.4f}")
            print(f"b:                  {resultados['b']:.4f}")
        elif resultados['model'] == "polinomica":
            print(f"Grado:              {resultados['grado']}")
            print(f"Coeficientes:       {[round(c, 4) for c in resultados['coeffs']]}")
        print(f"Correlación (r):    {resultados['r']:.4f}")
        print(f"Determinación (R²): {resultados['r2']:.4f} ({resultados['r2']*100:.2f}%)")
        print(f"Error estándar (s): {resultados['s']:.4f}")
        print(f"SSR:                {resultados['SSR']:.4f}")
        print(f"SSE:                {resultados['SSE']:.4f}")
        print(f"SST:                {resultados['SST']:.4f}")
        print("================================")

        if user_f.binary_question("\n¿Desea ver la gráfica de dispersión y curva de regresión?", "s/n"):
            num_f.graficar_regresion(x, y, resultados)

        predecir = user_f.binary_question("¿Desea predecir un valor de Y dado un X?", "s/n")
        while predecir:
            try:
                x_pred = float(input("Ingrese el valor de X: "))
                if resultados["model"] == "logaritmica" and x_pred <= 0:
                    print("Error: Para el modelo logarítmico, X debe ser > 0.")
                else:
                    y_pred = resultados["predict"](x_pred)
                    print(f"  Ŷ = {y_pred:.4f}")
            except ValueError:
                print("Error. Ingrese un número válido.")
            except Exception as e:
                print(f"Error en la predicción: {e}")
            predecir = user_f.binary_question("¿Desea predecir otro valor?", "s/n")

if __name__ == "__main__":
    x = Tabla()