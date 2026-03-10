import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from pywaffle import Waffle

class EcobiciViz:
    def render_map_and_waffle(self, df):
        # ... (lógica de datos y controles igual que antes)

        # Usamos columnas con proporciones ajustadas y sin "gap" (espacio entre ellas)
        col_mapa, col_waffle = st.columns([2.5, 1], gap="small")

        with col_mapa:
            # Quitamos los márgenes de Plotly para que toque los bordes
            fig_map = px.scatter_mapbox(
                # ... tus parámetros del mapa
                height=650 
            )
            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0}, # 0 margen en todos los lados
                showlegend=False
            )
            st.plotly_chart(fig_map, use_container_width=True)

        with col_waffle:
            # Usamos un contenedor de Streamlit para controlar el título
            st.markdown(f"#### {seleccion}")
            
            if sum(valores_waffle) > 0:
                fig = plt.figure(
                    FigureClass=Waffle,
                    rows=n_rows,
                    values=valores_waffle,
                    # ... tus colores e iconos
                    figsize=(8, 12),
                    legend={
                        'loc': 'lower center', 
                        'bbox_to_anchor': (0.5, -0.1),
                        'ncol': 2,
                        'frameon': False
                    }
                )
                
                # LA CLAVE: subplot_adjust con márgenes negativos o cero
                # right=1.0 para que toque el borde derecho
                plt.subplots_adjust(left=0, right=1.0, top=1, bottom=0.1)
                
                # st.pyplot con bbox_inches='tight' para recortar espacios sobrantes
                st.pyplot(fig, use_container_width=True, bbox_inches='tight', pad_inches=0)
                st.caption(f"**Escala:** {escala_txt}")
