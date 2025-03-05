import streamlit as st
from components.navigation import render_sidebar
from components.inicio.container_mis_facturas import render_misfacturas
from components.inicio.container_economia import render_economia

# st.set_page_config(page_title="FacturIA", layout="wide")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Mis facturas"

render_sidebar()

if st.session_state.pagina == "Mis facturas":
    render_economia()
    render_misfacturas()
else:
    st.title("Página no encontrada")
