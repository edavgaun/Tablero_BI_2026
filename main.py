import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------------------------------------
st.set_page_config(
    page_title="Tablero de Inteligencia de Negocios",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Tablero Interactivo – Inteligencia de Negocios")
st.caption("Universidad Panamericana · Campus CDMX")

# -----------------------------------------------------------
# CARGA DE DATOS
# -----------------------------------------------------------
@st.cache_data    # Python decorator
def load_data():
    url="UBER dataset.xlsx"
    all_sheets = pd.read_excel(url, sheet_name=None)
    return all_sheets['Switchbacks']

df = load_data()

# -----------------------------------------------------------
# PESTAÑAS PRINCIPALES
# -----------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Documentación General", "🔍 Datos", "📊 Gráficas"])

# -----------------------------------------------------------
# TAB 1: Documentación General
# -----------------------------------------------------------
with tab1:
    st.subheader("Documentación general del tablero")

    st.markdown("""# 🧠 Tablero Interactivo de Inteligencia de Negocios

## Universidad Panamericana · Campus Ciudad de México
<img src="https://posgrados-panamericana.up.edu.mx/hs-fs/hubfs/logo%20posgrados%20con%20espacio.png?width=137&name=logo%20posgrados%20con%20espacio.png" width=150>

Este repositorio contiene un tablero interactivo desarrollado para las actividades de la clase de **Inteligencia de Negocios**. Su propósito es ofrecer a los estudiantes una herramienta práctica para explorar datos, aplicar conceptos vistos en clase y comprender cómo se construye una solución analítica moderna usando Streamlit.

---

## 🎯 Objetivo del Proyecto

El tablero permite a los estudiantes:

* Manipular un conjunto de datos real o sintético.
* Aplicar filtros, segmentaciones y selecciones para generar visualizaciones dinámicas.
* Comprender la lógica detrás de una herramienta de Business Intelligence.
* Experimentar con decisiones basadas en datos y narrativas visuales.

Este proyecto sirve como puente entre los conceptos teóricos y la aplicación práctica en un entorno interactivo similar al utilizado en empresas.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.10+**
* **Streamlit** para la creación del tablero.
* **Pandas** para manipulación y limpieza de datos.
* **Plotly** para visualizaciones interactivas.
* Otros paquetes según la actividad.

---

## 📂 Estructura del Repositorio

```
📦 proyecto-bi-dashboard
│
├── app.py              # Archivo principal del dashboard
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Este archivo
```

---

## 📊 Sobre el Dataset

El dataset utilizado está pensado para que los estudiantes puedan:

* Probar diferentes tipos de visualizaciones.
* Explorar patrones y relaciones entre variables.
* Identificar oportunidades de negocio basadas en datos.

Si deseas cambiar el dataset, solo reemplázalo en la carpeta `data/` y asegúrate de ajustar el código si cambian los nombres de las columnas.""")



# -----------------------------------------------------------
# TAB 2: Comparaciones
# -----------------------------------------------------------
with tab2:
    st.subheader("Dataset del ejercicio")

    st.write("Selecciona el rango de observaciones que deseas visualizar:")

    # Slider de rango equivalente a IntRangeSlider de ipywidgets
    start, end = st.slider(
        "Rango de filas:",
        min_value=0,
        max_value=len(df),
        value=(0, len(df)),   # valor inicial: toda la tabla
        step=1
    )

    # Mostrar sección del dataframe
    st.dataframe(df.iloc[start:end])

# -----------------------------------------------------------
# TAB 3: Resumen e Insights
# -----------------------------------------------------------
with tab3:
    st.subheader("Visualizaciones")

    st.write("Hola Mundo")
