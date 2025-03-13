import streamlit as st
from components.main.logout import logout

flag_button = True
flag_factura = False
flag_image = False

st.radio(
    "Elija el tipo de factura",
    ["Venta", "Compra"],
    key="tipo_factura",
    horizontal=True,
    index=None
)
if "tipo_factura" in st.session_state:
    flag_factura = True
    tipo_factura_seleccionado = st.session_state.tipo_factura


uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    flag_image = True
    st.image(uploaded_file, caption="imagen_factura")
if flag_image & flag_factura != False:
    flag_button = False

st.button("Confirmar",disabled=flag_button)

logout().logoutbutton()
