import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from pywaffle import Waffle

class EcobiciViz:
    def render_map_and_waffle(self, df):
        # --- CONFIGURACIÓN EN SIDEBAR ---
        st.sidebar.markdown("### Controles de Visualización")
        estaciones = ["Todas"] + sorted(df['name'].unique().tolist())
        seleccion = st.sidebar.selectbox("Selecciona una estación:", estaciones)
        nivel_slider = st.sidebar.slider("Nivel de Zoom", 1, 4, 1)
        tamanio_puntos_mapa = st.sidebar.slider("Tamaño puntos mapa", 10, 40, 15)
        
        columnas_status = ['num_bikes_available', 'num_bikes_disabled', 
                           'num_docks_available', 'num_docks_disabled']
        
        # --- LÓGICA DE DATOS ---
        if seleccion != "Todas":
            fila = df[df['name'] == seleccion].iloc[0]
            valores_waffle = fila[columnas_status].values.astype(int)
            lat_center, lon_center = fila['lat'], fila['lon']
            n_rows = 4  # Menos filas para que los iconos sean Gigantes
            escala_txt = "1 icono = 1 unidad"
        else:
            factor = 100
            valores_waffle = (df[columnas_status].sum().values / factor).astype(int)
            lat_center, lon_center = df['lat'].mean(), df['lon'].mean()
            n_rows = 10 # Distribución para vista global
            escala_txt = f"1 icono ≈ {factor} unidades"

        # --- DISEÑO DE COLUMNAS ---
        col_mapa, col_waffle = st.columns([2, 1])

        with col_mapa:
            df['size_marker'] = tamanio_puntos_mapa
            df['resaltado'] = df['name'].apply(lambda x: 'Seleccionada' if x == seleccion else 'Normal')
            
            fig_map = px.scatter_mapbox(
                df, lat="lat", lon="lon", size="size_marker", size_max=tamanio_puntos_mapa,
                color="resaltado", color_discrete_map={"Seleccionada": "red", "Normal": "#1f77b4"},
                zoom={1: 12, 2: 13.5, 3: 15, 4: 16.5}[nivel_slider],
                center={"lat": lat_center, "lon": lon_center},
                mapbox_style="carto-positron", height=600 # Altura fija para el mapa
            )
            
            if seleccion != "Todas":
                fig_map.add_trace(go.Scattermapbox(
                    lat=[lat_center], lon=[lon_center], mode='markers',
                    marker=go.scattermapbox.Marker(size=tamanio_puntos_mapa+15, color='red', symbol='marker')
                ))
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
            st.plotly_chart(fig_map, use_container_width=True)

        with col_waffle:
            st.markdown(f"### {seleccion if seleccion != 'Todas' else 'Total Ciudad'}")
            
            if sum(valores_waffle) > 0:
                # CREACIÓN DEL WAFFLE GIGANTE
                fig = plt.figure(
                    FigureClass=Waffle,
                    rows=n_rows,
                    values=valores_waffle,
                    colors=["#2ecc71", "#e74c3c", "#3498db", "#95a5a6"],
                    icons='bicycle',
                    font_size=45,       # <--- ICONOS MUCHO MÁS GRANDES
                    figsize=(7, 12),    # <--- FIGURA ALTA PARA LLENAR LA COLUMNA
                    icon_legend=True,
                    legend={
                        'labels': ['Disponible', 'Dañada', 'Libre', 'Dañado'],
                        'loc': 'lower center', 
                        'bbox_to_anchor': (0.5, -0.1), 
                        'ncol': 2,
                        'fontsize': 12,
                        'frameon': False
                    }
                )
                
                # Forzar a que no haya márgenes blancos en la imagen generada
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0.1)
                
                # El parámetro use_container_width=True es clave aquí
                st.pyplot(fig, use_container_width=True, clear_figure=True)
                st.caption(f"**Escala:** {escala_txt}")
            else:
                st.info("Sin datos para graficar.")
