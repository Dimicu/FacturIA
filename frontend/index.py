from time import sleep
from pages.login import login_page
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="FacturIA")
st.title("Mainpage")
# Sidebar
with st.sidebar:

    st.sidebar.success("Elije un apartado")

if __name__ == "__main__":
    login_page()
