import plotly.express as px
import plotly.graph_objects as go # Importación necesaria para el marcador extra
import streamlit as st
import numpy as np

class EcobiciViz:
    def render_map(self, df):
        st.subheader("Mapa Interactivo de Estaciones Ecobici")
        
        if df.empty:
            st.warning("No hay datos disponibles para mostrar el mapa.")
            return

        # --- CONTROLES (Sidebar para no saturar el mapa) ---
        st.sidebar.markdown("### Configuración del Mapa")
        
        # 1. Lista desplegable para resaltar estación
        estaciones = ["Todas"] + sorted(df['name'].unique().tolist())
        seleccion = st.sidebar.selectbox("Busca y selecciona una estación:", estaciones)

        # 2. Slider de Zoom (4 niveles)
        # Mapeamos Niveles 1-4 a valores de zoom de Mapbox (aprox 12-16)
        zoom_level_map = {1: 12, 2: 13.3, 3: 14.6, 4: 16}
        nivel_slider = st.sidebar.slider("Nivel de Zoom", min_value=1, max_value=4, value=1, step=1)
        zoom_val = zoom_level_map[nivel_slider]

        # 3. Control de tamaño base de la estación
        tamanio_base = st.sidebar.slider("Tamaño de punto de estación", min_value=10, max_value=30, value=15)


        # --- LÓGICA DE CENTRADO Y RESALTADO ---
        
        # Creamos una columna temporal para el tamaño (para agrandar los puntos)
        df['size_marker'] = tamanio_base 

        df_seleccionada = None

        if seleccion != "Todas":
            # Marcamos la seleccionada para el color de la capa base
            df['resaltado'] = df['name'].apply(lambda x: 'Seleccionada' if x == seleccion else 'Normal')
            color_map = {"Seleccionada": "#FF4B4B", "Normal": "#1f77b4"}
            
            # Obtener coordenadas para centrar el mapa en la estación
            punto = df[df['name'] == seleccion].iloc[0]
            lat_center, lon_center = punto['lat'], punto['lon']
            
            # Guardamos el dataframe de la estación seleccionada para el marcador extra
            df_seleccionada = df[df['name'] == seleccion]

        else:
            df['resaltado'] = 'Normal'
            color_map = {"Normal": "#1f77b4"}
            # Centrar en el centroide de TODAS las estaciones
            lat_center = df['lat'].mean()
            lon_center = df['lon'].mean()


        # --- CREACIÓN DEL MAPA BASE (Plotly Express) ---
        fig = px.scatter_mapbox(
            df,
            lat="lat",
            lon="lon",
            size="size_marker", # Variable que controla el tamaño
            size_max=tamanio_base, # Límite máximo del tamaño
            hover_name="name",
            hover_data={
                "lat": False, 
                "lon": False, 
                "capacity": True,
                "num_bikes_available": True,
                "size_marker": False, # No mostrar en hover
                "resaltado": False   # No mostrar en hover
            },
            color="resaltado",
            color_discrete_map=color_map,
            zoom=zoom_val, # Zoom definido por el slider
            center={"lat": lat_center, "lon": lon_center},
            height=700
        )

        # --- AÑADIR MARCADOR EXTRA A LA SELECCIÓN (Plotly Graph Objects) ---
        if df_seleccionada is not None:
            fig.add_trace(go.Scattermapbox(
                lat=df_seleccionada['lat'],
                lon=df_seleccionada['lon'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=25,          # Marcador grande
                    color='rgb(255, 0, 0)', # Rojo puro
                    symbol='marker'    # Símbolo de "pin" o marcador
                ),
                hoverinfo='none',      # El hover lo maneja la capa base
                showlegend=False
            ))

        # Estilo visual del mapa
        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        
        # Publicar mapa
        st.plotly_chart(fig, use_container_width=True)
