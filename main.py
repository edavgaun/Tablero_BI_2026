import streamlit as st

# Configuración inicial
st.set_page_config(layout="wide", page_title="Ecobici Dashboard UP")

# CSS con margen pequeño y elegante
st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem !important;    /* Espacio arriba del encabezado */
            padding-bottom: 1rem !important;
            padding-left: 2rem !important;     /* Margen izquierdo sutil */
            padding-right: 2rem !important;    /* Margen derecho sutil */
        }
        header {visibility: hidden;}           /* Mantenemos limpio el techo */
        
        /* Ajuste para que los widgets no estén pegados al borde del sidebar */
        .css-1d391kg { padding: 1.5rem 1rem; }
    </style>
    """, unsafe_allow_html=True)

# ... resto de tus imports (Header, Service, Viz)
