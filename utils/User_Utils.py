import os
import pandas as pd

def select_option(options:list, text:str):
    """Muestra un menu de opciones y devuelve el valor 
    seleccionado de la lista. (NO el indice).
    Ejemplo: options = ["Manzanas", "Peras", "Mangos"]
    Si el usuario selecciona 2, se devuelve "Peras"""

    while True:
        print(text)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            eleccion = int(input("Ingrese el numero de la opcion: "))
            if 1 <= eleccion <= len(options):
                return options[eleccion - 1]
            else:
                print("\n","-"*4,"Opcion invalida, intente de nuevo.","-"*4,"\n")
        except ValueError:
            print("\n","-"*4,"Entrada invalida. Por favor ingrese un numero.","-"*4,"\n")

def binary_question(question:str, answers:str="s/n"):
    """
    Pregunta al usuario una pregunta de si/no y devuelve True o False.
    
    :param question: Texto a mostrar al usuario
    :param answers: String con las opciones validas, por defecto "s/n" (Solo pueden ser 3 caracteres, el primero es la opcion positiva y el segundo la negativa)
    :return: True si el usuario responde 's', False si responde 'n'
    """
    while True:
        respuesta = input(f"{question} ({answers}): ").lower()
        if respuesta == answers[0] or respuesta == answers[2]:
            return True if respuesta == answers[0] else False
        else:
            print("Respuesta invalida. Por favor ingrese una opcion valida.")

def get_positive_integer(prompt:str):
    """Solicita al usuario que ingrese un numero entero positivo y lo devuelve.
    Si el usuario ingresa un valor no valido, se le vuelve a solicitar hasta que ingrese un valor correcto."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Error. Por favor ingrese un numero entero positivo.")
        except ValueError:
            print("Error. Por favor ingrese un numero entero positivo.")

def get_table(path_tablas, header=None):
    """Solicita al usuario el nombre de una tabla y 
    devuelve un DataFrame con los datos de esa tabla.
    :param path_tablas: Ruta de la carpeta donde se encuentran las tablas
    :param header: Indica si la tabla tiene encabezado o no. Por defecto es None (sin encabezado). Si se establece en 0, la primera fila se considerará como encabezado.
    :return: DataFrame con los datos de la tabla seleccionada por el usuario"""
    while True:
        nombre_tabla = input("Ingrese el nombre de la tabla (sin extension): ")
        path_tabla = os.path.join(path_tablas, f"{nombre_tabla}.csv")
        if not os.path.exists(path_tabla):
            print("Error. La tabla no existe.")
        else:
            return pd.read_csv(path_tabla, header=header)