import streamlit as st

# Configuración de la página
st.set_page_config(page_title="FacturIA")

# Verificar si el usuario ha iniciado sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Si el usuario está autenticado, mostrar la MainPage
if st.session_state.authenticated:
    pageManager = st.navigation([
        st.Page("main.py", title="Principal", default=True)
    ])
else:
    pageManager = st.navigation([
        st.Page("home.py", title="Inicio", default=True),
        st.Page("pages/login.py", title="Login"),
        st.Page("pages/registro.py", title="Registro")
    ])

pageManager.run()
