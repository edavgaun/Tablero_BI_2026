from Modules.UI.header import show_header
from Modules.Data.ecobici_service import EcobiciService
from Modules.Viz.viz_service import EcobiciViz
import streamlit as st

show_header("Dashboard Ecobici UP Mixcoac")

ecobici = EcobiciService()
df = ecobici.get_full_data()

if not df.empty:
    viz = EcobiciViz()
    # Llamamos a la nueva función que organiza ambos gráficos
    viz.render_map_and_waffle(df)
