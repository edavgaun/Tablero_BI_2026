import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from pywaffle import Waffle

class EcobiciViz:
    def render_map_and_waffle(self, df):
        # --- CONTROLES EN SIDEBAR ---
        st.sidebar.markdown("### Configuración")
        estaciones = ["Todas"] + sorted(df['name'].unique().tolist())
        seleccion = st.sidebar.selectbox("Selecciona una estación:", estaciones)
        
        nivel_slider = st.sidebar.slider("Nivel de Zoom", 1, 4, 1)
        zoom_map = {1: 12, 2: 13.5, 3: 15, 4: 16.5}
        
        # --- PREPARACIÓN DE DATOS ---
        columnas_status = ['num_bikes_available', 'num_bikes_disabled', 
                           'num_docks_available', 'num_docks_disabled']
        
        if seleccion != "Todas":
            df_plot = df[df['name'] == seleccion].copy()
            fila = df_plot.iloc[0]
            valores_waffle = fila[columnas_status].values
            titulo_waffle = f"Estado: {seleccion}"
            # Centrado en la estación
            lat_center, lon_center = fila['lat'], fila['lon']
            # Marcador resaltado
            df['resaltado'] = df['name'].apply(lambda x: 'Seleccionada' if x == seleccion else 'Normal')
        else:
            # Estado global de la ciudad
            valores_waffle = df[columnas_status].sum().values
            titulo_waffle = "Estado Global de Ecobici CDMX"
            # Centrado en el promedio
            lat_center, lon_center = df['lat'].mean(), df['lon'].mean()
            df['resaltado'] = 'Normal'

        # --- DISEÑO EN COLUMNAS ---
        col_mapa, col_waffle = st.columns([2, 1]) # El mapa es el doble de ancho

        with col_mapa:
            st.subheader("Ubicación")
            fig_map = px.scatter_mapbox(
                df, lat="lat", lon="lon",
                color="resaltado",
                color_discrete_map={"Seleccionada": "#FF4B4B", "Normal": "#1f77b4"},
                zoom=zoom_map[nivel_slider],
                center={"lat": lat_center, "lon": lon_center},
                mapbox_style="carto-positron",
                height=500
            )
            
            if seleccion != "Todas":
                fig_map.add_trace(go.Scattermapbox(
                    lat=[lat_center], lon=[lon_center],
                    mode='markers',
                    marker=go.scattermapbox.Marker(size=20, color='red', symbol='marker'),
                    showlegend=False
                ))
            
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
            st.plotly_chart(fig_map, use_container_width=True)

        with col_waffle:
            st.subheader("Disponibilidad")
            
            # Cálculo de filas dinámicas para el Waffle
            total_items = sum(valores_waffle)
            n_rows = max(1, int(total_items // 15)) if seleccion != "Todas" else 30
            
            fig_waffle = plt.figure(
                FigureClass=Waffle,
                rows=n_rows,
                values=valores_waffle,
                colors=["#2ecc71", "#e74c3c", "#3498db", "#95a5a6"],
                legend={
                    'labels': ['Disponible', 'Dañada', 'Puerto Libre', 'Puerto Dañado'],
                    'loc': 'lower left',
                    'bbox_to_anchor': (0, -0.2),
                    'ncol': 2,
                    'fontsize': 10
                },
                icons='bicycle',
                font_size=12,
                figsize=(5, 8)
            )
            st.pyplot(fig_waffle)
            st.caption(f"Capacidad total representada: {int(total_items)}")
