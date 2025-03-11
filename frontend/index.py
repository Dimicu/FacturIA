import streamlit as st

# Configuración de la página
st.set_page_config(page_title="FacturIA")

# Verificar si el usuario ha iniciado sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Si el usuario está autenticado, mostrar la MainPage
if st.session_state.authenticated:
    pageManager = st.navigation([
        st.Page("views/main/main.py", title="Mis facturas", default=True),
        st.Page("views/main/anadir_facturas.py", title="Añadir facturas")
    ])
else:
    pageManager = st.navigation([
        st.Page("views/home/home.py", title="Inicio", default=True),
        st.Page("views/home/login.py", title="Login"),
        st.Page("views/home/registro.py", title="Registro")
    ])

pageManager.run()
