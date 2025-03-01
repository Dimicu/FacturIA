import streamlit as st
from .sidebar import side_bar_button_style

# Opciones del menú
MENU_OPCIONES = {
    "Mis facturas": "Mis facturas",
    "anadir_factura": "anadir_factura",
}


def cambiar_pagina():
    st.session_state.pagina = st.session_state.nueva_pagina


def render_sidebar():
    user = "User"
    user_picture = "https://imgs.search.brave.com/JAHeWxUYEwHB7KV6V1IbI9oL7wxJwIQ4Sbp8dHQL09A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMjAx/MzkxNTc2NC9waG90/by91c2VyLWljb24t/aW4tZmxhdC1zdHls/ZS5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9UEotMnZvUWZh/Q3hhZUNsdzZYYlVz/QkNaT3NTTjlIVWVC/SUg1Qk82VmRScz0"

    with st.sidebar:
        col1, col2 = st.columns(2)
        col1.image(user_picture, width=150)
        col2.markdown(f"<h3>{user}</h3>", unsafe_allow_html=True)
        st.divider()

        # Botones del menú
        for nombre, valor in MENU_OPCIONES.items():
            if nombre != "anadir_factura":
                if st.markdown(side_bar_button_style(nombre), unsafe_allow_html=True):
                    st.session_state.nueva_pagina = valor
                    cambiar_pagina()
