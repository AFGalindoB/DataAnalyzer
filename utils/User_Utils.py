import os
import pandas as pd
import sys
import subprocess


def open_file_dialog():
    """
    Abre el explorador de archivos nativo del sistema operativo para seleccionar
    un archivo CSV. Compatible con Windows, Linux (X11/Wayland) y Raspberry Pi OS.

    Retorna la ruta absoluta del archivo seleccionado, o None si se cancela.
    """
    system = sys.platform  # 'win32', 'linux', 'darwin'

    # ── Windows ──────────────────────────────────────────────────────────────
    if system == "win32":
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()          # ocultar ventana principal
            root.attributes("-topmost", True)
            ruta = filedialog.askopenfilename(
                title="Seleccionar archivo CSV",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            )
            root.destroy()
            return ruta if ruta else None
        except Exception as e:
            print(f"[GUI] Error al abrir el explorador en Windows: {e}")
            return _fallback_manual()

    # ── Linux / Raspberry Pi OS ───────────────────────────────────────────────
    elif system == "linux":
        ruta = _linux_file_dialog()
        return ruta if ruta else None

    # ── macOS (bonus) ─────────────────────────────────────────────────────────
    elif system == "darwin":
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            ruta = filedialog.askopenfilename(
                title="Seleccionar archivo CSV",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            )
            root.destroy()
            return ruta if ruta else None
        except Exception as e:
            print(f"[GUI] Error al abrir el explorador en macOS: {e}")
            return _fallback_manual()

    else:
        print(f"Sistema operativo '{system}' no reconocido.")
        return _fallback_manual()


def _linux_file_dialog():
    """
    Intenta abrir un diálogo de archivos en Linux usando múltiples backends,
    en orden de prioridad. Funciona en escritorios Wayland, X11 y entornos
    headless como la Raspberry Pi con display conectado.
    """

    # 1. zenity  — disponible en GNOME, Raspberry Pi OS con escritorio
    if _comando_existe("zenity"):
        try:
            resultado = subprocess.run(
                ["zenity", "--file-selection",
                 "--title=Seleccionar archivo CSV",
                 "--file-filter=*.csv"],
                capture_output=True, text=True
            )
            ruta = resultado.stdout.strip()
            return ruta if ruta else None
        except Exception:
            pass

    # 2. kdialog — disponible en KDE
    if _comando_existe("kdialog"):
        try:
            resultado = subprocess.run(
                ["kdialog", "--getopenfilename", os.path.expanduser("~"), "*.csv",
                 "--title", "Seleccionar archivo CSV"],
                capture_output=True, text=True
            )
            ruta = resultado.stdout.strip()
            return ruta if ruta else None
        except Exception:
            pass

    # 3. yad    — alternativa a zenity con más opciones
    if _comando_existe("yad"):
        try:
            resultado = subprocess.run(
                ["yad", "--file-selection",
                 "--title=Seleccionar archivo CSV",
                 "--file-filter=CSV files (*.csv) | *.csv"],
                capture_output=True, text=True
            )
            ruta = resultado.stdout.strip()
            return ruta if ruta else None
        except Exception:
            pass

    # 4. tkinter — fallback GUI puro Python (requiere python3-tk instalado)
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        root.destroy()
        return ruta if ruta else None
    except Exception:
        pass

    # 5. Sin GUI disponible → ingresar ruta manualmente
    print("[GUI] No se encontró ningún explorador de archivos gráfico disponible.")
    return _fallback_manual()


def _comando_existe(cmd):
    """Verifica si un comando existe en el PATH del sistema."""
    return subprocess.call(
        ["which", cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 0


def _fallback_manual():
    """Pide la ruta del archivo manualmente si no hay GUI disponible."""
    print("Ingrese la ruta del archivo CSV manualmente.")
    ruta = input("Ruta: ").strip().strip('"').strip("'")
    if os.path.isfile(ruta):
        return ruta
    print(f"Error: no se encontró el archivo '{ruta}'")
    return None

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

def seleccionar_tabla(path_tablas):
    """Muestra las tablas disponibles y devuelve la ruta completa del archivo seleccionado.
    No lee el CSV todavía."""
    
    archivos = [f for f in os.listdir(path_tablas) if f.endswith(".csv")]
    
    if not archivos:
        print("No hay tablas disponibles en la carpeta.")
        return None
    
    print("\nTablas disponibles:")
    for i, nombre in enumerate(archivos, start=1):
        print(f"  {i}. {nombre.replace('.csv', '')}")
    
    while True:
        try:
            opcion = int(input("\nIngrese el número de la tabla: "))
            if 1 <= opcion <= len(archivos):
                return os.path.join(path_tablas, archivos[opcion - 1])
            print(f"Error. Ingrese un número entre 1 y {len(archivos)}.")
        except ValueError:
            print("Error. Ingrese un número válido.")


def obtener_datos_tabla(path_tabla):
    """Carga una tabla seleccionada por el usuario y la devuelve como DataFrame.
    
    Parámetros:
        path_tabla: Ruta completa del archivo CSV
    
    Retorna:
        DataFrame con los datos de la tabla, o None si no se pudo cargar.
    """
    if path_tabla is None or not os.path.exists(path_tabla):
        print("Error: No se encontró la ruta de la tabla.")
        return None

    tiene_encabezados = binary_question("¿La tabla tiene encabezados?", "s/n")
    header = 0 if tiene_encabezados else None

    df = pd.read_csv(path_tabla, header=header)

    print(f"\nTabla cargada: {os.path.basename(path_tabla)}")
    print(f"Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")

    if tiene_encabezados and df.shape[1] > 1:
        # Caso con encabezados y múltiples columnas → elegir columna
        headers = df.columns.tolist()
        columna_elegida = select_option(headers, "Seleccione la columna que desea usar:")
        datos = df[columna_elegida].to_numpy(dtype=float)
        print(f"Usando columna: {columna_elegida}")
    else:
        # Caso sin encabezados o tabla de una sola columna → aplanar todo
        datos = df.to_numpy().flatten().astype(float)
        print("Usando todos los datos (matriz aplanada)")

    print(f"Datos listos: {len(datos)} valores")
    print("-" * 60)
    return datos