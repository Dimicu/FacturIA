import streamlit as st
from components.main.logout import logout

if "layoutConfig" not in st.session_state:
    st.session_state["layoutConfig"] = "centered"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "edit_factura" not in st.session_state:
    st.session_state["edit_factura"] = ""
if "anadir_factura" not in st.session_state:
    st.session_state["anadir_factura"] = ""
if "imagen_factura" not in st.session_state:
    st.session_state["imagen_factura"] = ""


st.set_page_config(page_title="FacturIA",layout=st.session_state["layoutConfig"])

if st.session_state.authenticated:
    pageManager = st.navigation([
        st.Page("views/main/main.py", title="Mis facturas", default=True),
        st.Page("views/main/anadir_facturas.py", title="Añadir facturas")
    ])
    if st.session_state["anadir_factura"] != "":
        pageManager = st.navigation([
            st.Page("views/main/anadir_facturas_form.py", title="Mis facturas", default=True)
        ])
    if st.session_state["edit_factura"] != "":
        pageManager = st.navigation([
            st.Page("views/main/editar_facturas_form.py", title="Mis facturas", default=True)
        ])
    # if st.session_state["edit_factura"] == "" or st.session_state["anadir_factura"] == "":
    #     st.sidebar.title(st.session_state['email'].split('@')[0].capitalize())
    #     logout().logoutbutton()
else:
    pageManager = st.navigation([
        st.Page("views/home/home.py", title="Inicio", default=True),
        st.Page("views/home/login.py", title="Login"),
        st.Page("views/home/registro.py", title="Registro")
    ])

pageManager.run()
