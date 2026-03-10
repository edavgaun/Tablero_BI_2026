import streamlit as st

# ESTA DEBE SER LA LÍNEA 1 (después de los imports de librerías base)
st.set_page_config(layout="wide", page_title="Ecobici Dashboard UP")

# Inyección de CSS corregida y segura
st.markdown("""
    <style>
        /* Margen de cortesía en los bordes de la app */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }
        /* Ocultar elementos innecesarios */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Ahora sí, el resto de las importaciones de tus módulos
try:
    from Modules.UI.header import show_header
    from Modules.Data.ecobici_service import EcobiciService
    from Modules.Viz.viz_service import EcobiciViz
except Exception as e:
    st.error(f"Error al importar módulos: {e}")

# --- EJECUCIÓN DEL TABLERO ---

def main():
    # Encabezado
    show_header("Análisis de Movilidad: Ecobici CDMX")
    
    # Instanciar servicios
    service = EcobiciService()
    viz = EcobiciViz()
    
    # Carga de datos
    with st.spinner('Cargando datos de la API de Ecobici...'):
        df = service.get_full_data()
    
    if df is not None and not df.empty:
        # Ejecutar la visualización que creamos en viz_service.py
        viz.render_map_and_waffle(df)
    else:
        st.error("No se pudieron obtener datos. Verifica tu conexión o la API de Ecobici.")

if __name__ == "__main__":
    main()
