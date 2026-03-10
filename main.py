# Sección de importación de módulos
from Modules.UI.header import show_header
from Modules.Data.ecobici_service import EcobiciService

# Sección para crear la GUI
show_header("Mi primera GUI en Streamlit")

ecobici = EcobiciService()
# Cargar datos
df = ecobici.get_full_data()

st.write(df)
