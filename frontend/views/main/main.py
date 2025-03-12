import streamlit as st
from components.inicio.container_mis_facturas import misfacturasclass
from components.inicio.container_economia import economiaclass
from components.main.logout import logout

# st.set_page_config(page_title="FacturIA", layout="wide")

economiaclass().render_economia()
misfacturasclass().misfacturas()


