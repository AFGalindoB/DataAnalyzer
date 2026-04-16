# DataAnalyzer

DataAnalyzer es una herramienta de análisis estadístico en consola desarrollada en Python.  
Permite crear tablas de datos, generar tablas de frecuencias, calcular estadísticas descriptivas y visualizar distribuciones mediante gráficos de tallos y hojas.

---

## Funcionalidades actuales

### Gestión de Tablas
- **Crear tabla**: Crea una tabla personalizada definiendo filas, columnas y tipo de dato (entero/decimal). Se guarda automáticamente en formato `.csv`.
- **Agregar tabla desde archivo**: Permite seleccionar un archivo `.csv` mediante el explorador de archivos nativo del sistema (Windows, Linux y macOS). Soporta tablas con o sin encabezados.

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

### Regresiones
Permite realizar regresiones con las siguientes opciones:

- **Regresión Lineal** (`Y = β₀ + β₁X`)
- **Regresión Exponencial** (`Y = a · e^(bX)`)
- **Regresión Logarítmica** (`Y = a + b · ln(X)`)
- **Regresión Polinómica** (de grado configurable)

**Características comunes en todas las regresiones:**
- Filtrado opcional de datos atípicos (métodos: IQR, Recorte por porcentaje, Z-score)
- Cálculo completo de estadísticos: correlación (r), coeficiente de determinación (R²), error estándar, SSR, SSE y SST
- Gráfica de dispersión con la curva de regresión
- Gráfica de residuos
- Predicción interactiva de valores de Y dado un X

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
