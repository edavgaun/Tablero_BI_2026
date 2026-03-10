import streamlit as st

# DEBE SER LA PRIMERA LÍNEA DESPUÉS DE LOS IMPORTS
st.set_page_config(layout="wide", page_title="Ecobici Dashboard")

# Inyectamos el CSS para eliminar los márgenes superiores y laterales
st.markdown("""
    <style>
        /* Eliminar espacio superior */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        /* Eliminar barra de menú superior */
        header {visibility: hidden;}
        /* Ajustar el canvas del gráfico para que pegue a la derecha */
        .stPlotlyChart {
            margin-bottom: -2rem;
        }
    </style>
    """, unsafe_allow_html=True)

from Modules.UI.header import show_header
from Modules.Data.ecobici_service import EcobiciService
from Modules.Viz.viz_service import EcobiciViz

# Tu lógica actual
show_header("Mi primera GUI en Streamlit")

ecobici = EcobiciService()
df = ecobici.get_full_data()

if not df.empty:
    viz = EcobiciViz()
    viz.render_map_and_waffle(df)
