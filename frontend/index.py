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


st.set_page_config(page_title="FacturIA", layout=st.session_state["layoutConfig"])

profile = """<style>
*{
text-align: center;}
.sidebar-profile {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
.sidebar-profile img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid white;
}
</style>"""

if st.session_state.authenticated:
    pageManager = st.navigation(
        [
            st.Page("views/main/main.py", title="Mis facturas", default=True),
            st.Page("views/main/anadir_facturas.py", title="Añadir facturas"),
        ]
    )
    st.markdown(profile, unsafe_allow_html=True)
    if st.session_state["anadir_factura"] != "":
        pageManager = st.navigation(
            [
                st.Page(
                    "views/main/anadir_facturas_form.py",
                    title="Mis facturas",
                    default=True,
                )
            ]
        )
    if st.session_state["edit_factura"] != "":
        pageManager = st.navigation(
            [
                st.Page(
                    "views/main/editar_facturas_form.py",
                    title="Mis facturas",
                    default=True,
                )
            ]
        )
    if (
        st.session_state["edit_factura"] == ""
        and st.session_state["anadir_factura"] == ""
    ):

        with st.sidebar:
            st.sidebar.title(st.session_state["email"].split("@")[0].capitalize())
            st.markdown(
                '<div class="sidebar-profile"><img src="https://imgs.search.brave.com/TTWjkCnrJRF1di-RfGC9khqVzZWZd4beDFojTfD9KPk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cGl4YWJheS5jb20v/cGhvdG8vMjAyMy8w/Mi8xOC8xMS8wMC9p/Y29uLTc3OTc3MDRf/NjQwLnBuZw"></div>',
                unsafe_allow_html=True,
            )
        logout().logoutbutton()
else:
    pageManager = st.navigation(
        [
            st.Page("views/home/home.py", title="Inicio", default=True),
            st.Page("views/home/login.py", title="Login"),
            st.Page("views/home/registro.py", title="Registro"),
        ]
    )

pageManager.run()
