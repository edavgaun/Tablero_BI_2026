import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from pywaffle import Waffle

class EcobiciViz:
    def render_map_and_waffle(self, df):
        # --- CONTROLES EN SIDEBAR ---
        estaciones = ["Todas"] + sorted(df['name'].unique().tolist())
        seleccion = st.sidebar.selectbox("Selecciona una estación:", estaciones)
        nivel_slider = st.sidebar.slider("Nivel de Zoom", 1, 4, 1)
        tamanio_puntos = st.sidebar.slider("Tamaño puntos mapa", 10, 40, 15)
        
        columnas_status = ['num_bikes_available', 'num_bikes_disabled', 
                           'num_docks_available', 'num_docks_disabled']
        
        # --- LÓGICA DE CENTRADO Y ESCALA ---
        if seleccion != "Todas":
            fila = df[df['name'] == seleccion].iloc[0]
            valores_waffle = fila[columnas_status].values.astype(int)
            lat_c, lon_c = fila['lat'], fila['lon']
            n_rows, f_size = 5, 40
            escala = "1 icono = 1 unidad"
        else:
            factor = 100
            valores_waffle = (df[columnas_status].sum().values / factor).astype(int)
            lat_c, lon_c = df['lat'].mean(), df['lon'].mean()
            n_rows, f_size = 18, 25
            escala = f"1 icono ≈ {factor} unidades"

        # --- COLUMNAS SIN GAP ---
        col_mapa, col_waffle = st.columns([2.5, 1], gap="small")

        with col_mapa:
            df['resaltado'] = df['name'].apply(lambda x: 'Sel' if x == seleccion else 'Norm')
            
            # MAPA CORREGIDO (Sin comentarios internos que causen TypeError)
            fig_map = px.scatter_mapbox(
                df, lat="lat", lon="lon", 
                size=[tamanio_puntos]*len(df), size_max=tamanio_puntos,
                color="resaltado", 
                color_discrete_map={"Sel": "red", "Norm": "#1f77b4"},
                zoom={1: 12, 2: 13.5, 3: 15, 4: 16.5}[nivel_slider],
                center={"lat": lat_c, "lon": lon_c},
                mapbox_style="carto-positron", 
                height=750
            )
            
            if seleccion != "Todas":
                fig_map.add_trace(go.Scattermapbox(
                    lat=[lat_c], lon=[lon_c], mode='markers',
                    marker=go.scattermapbox.Marker(size=tamanio_puntos+15, color='red', symbol='marker')
                ))
            
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
            st.plotly_chart(fig_map, use_container_width=True)

        with col_waffle:
            st.markdown(f"#### {seleccion}")
            if sum(valores_waffle) > 0:
                fig = plt.figure(
                    FigureClass=Waffle,
                    rows=n_rows,
                    values=valores_waffle,
                    colors=["#2ecc71", "#e74c3c", "#3498db", "#95a5a6"],
                    icons='bicycle', font_size=f_size, figsize=(8, 14),
                    legend={'labels': ['Disp', 'Dañ', 'Libre', 'Dañ'], 
                            'loc': 'lower center', 'bbox_to_anchor': (0.5, -0.05), 
                            'ncol': 2, 'fontsize': 12, 'frameon': False}
                )
                # ELIMINAR ESPACIO A LA DERECHA DEL WAFFLE
                plt.subplots_adjust(left=0, right=1.0, top=1, bottom=0.1)
                st.pyplot(fig, use_container_width=True, bbox_inches='tight', pad_inches=0)
                st.caption(f"**Escala:** {escala}")
