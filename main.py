import streamlit as st

# Configuración de página para usar todo el ancho
st.set_page_config(layout="wide")

# CSS para eliminar espacios en blanco
st.markdown("""
    <style>
        # Eliminar el espacio superior (Header)
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        # Eliminar el espacio en blanco arriba del título
        header {visibility: hidden;}
        # Reducir el espacio entre widgets de la barra lateral
        .css-1d391kg {padding-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

# ... resto de tus imports y lógica
