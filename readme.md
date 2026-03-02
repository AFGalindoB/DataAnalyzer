# DataAnalyzer

DataAnalyzer es una herramienta de análisis estadístico en consola desarrollada en Python.  
Permite crear tablas de datos, generar tablas de frecuencias, calcular estadísticas descriptivas y visualizar distribuciones mediante gráficos de tallos y hojas.

---

## Funcionalidades actuales

### Crear tabla
- Permite crear una tabla personalizada.
- Define número de filas y columnas.
- Permite elegir si los datos serán enteros o decimales.
- Guarda la tabla automáticamente en formato `.csv` dentro de la carpeta `tablas/`.

---

### Realizar tabla de frecuencias
- Selecciona una tabla previamente creada.
- Permite definir la cantidad de clases.
- Genera intervalos dinámicos basados en los datos.
- Calcula frecuencias por clase usando `pandas`.

---

### Realizar gráfica de tallos y hojas
- Funciona con datos enteros o decimales.
- Permite definir la **escala de la hoja**.
- Genera la representación en consola organizada por tallos.

---

### Calcular muestra
Calcula automáticamente:

- Tamaño de muestra (n)
- Media
- Mediana
- Moda
- Varianza (muestral)
- Desviación estándar
- Cuartiles
- Rango intercuartílico

---

### Realizar gráfica de caja y bigotes

- Calcula automáticamente:
  - Q1 (primer cuartil)
  - Mediana
  - Q3 (tercer cuartil)
  - Rango intercuartílico (IQR)
  - Límites inferior y superior para detección de valores atípicos (1.5 × IQR)
- Genera una gráfica de caja y bigotes utilizando `matplotlib`.
- Permite visualizar:
  - Dispersión de los datos
  - Asimetría
  - Valores extremos (outliers)

---

### Realizar histograma

- Selecciona una tabla previamente creada.
- Permite definir la cantidad de clases (bins).
- Calcula automáticamente:
  - Media
  - Mediana
  - Valor mínimo
  - Valor máximo
- Genera un histograma utilizando `matplotlib`.
- Permite visualizar:
  - Distribución de los datos
  - Concentración de frecuencias
  - Forma de la distribución (simetría o sesgo)

---

## Tecnologías utilizadas

- `pandas`
- `numpy`
- `matplotlib`
- `collections`
- `os`
- `sys`

---

# Cómo ejecutar el proyecto por primera vez

Se recomienda usar un **entorno virtual** para mantener las dependencias aisladas.

```bash
python -m venv venv
venv\Scripts\activate
```


1. Clonar el repositorio

```bash
git clone https://github.com/AFGalindoB/DataAnalyzer.git
cd DataAnalyzer
```

2. Instalar las dependencias
```bash
pip install -r requirements.txt
```

3. Ejecutar el archivo main.py
