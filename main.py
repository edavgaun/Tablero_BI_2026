import streamlit as st

# 1. Configuración obligatoria al inicio
st.set_page_config(layout="wide", page_title="Ecobici Dashboard UP")

# 2. Inyección de CSS para eliminar espacios
st.markdown("""
    <style>
        /* Eliminar espacio superior y márgenes laterales del contenedor principal */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        /* Ocultar el header de Streamlit para ganar espacio arriba */
        header {visibility: hidden;}
        /* Eliminar espacio superior de los widgets */
        .stVerticalBlock {gap: 0rem;}
    </style>
    """, unsafe_allow_html=True)

from Modules.UI.header import show_header
from Modules.Data.ecobici_service import EcobiciService
from Modules.Viz.viz_service import EcobiciViz

# Título
show_header("Dashboard de BI - Universidad Panamericana")

# Lógica de datos
ecobici = EcobiciService()
df = ecobici.get_full_data()

if not df.empty:
    viz = EcobiciViz()
    viz.render_map_and_waffle(df)
