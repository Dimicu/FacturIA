import streamlit as st
import requests

flag_button = True
flag_factura = False
flag_image = False

st.radio(
    "Elija el tipo de factura",
    ["Venta", "Compra"],
    key="tipo_factura",
    horizontal=True,
    index=None,
)
if "tipo_factura" in st.session_state:
    flag_factura = True
    tipo_factura_seleccionado = st.session_state.tipo_factura


uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])


if uploaded_file is not None:
    flag_image = True
    st.image(uploaded_file, caption="imagen_factura")
if flag_image and flag_factura != False:
    flag_button = False

if st.button("Confirmar", disabled=flag_button):
    email = st.session_state.email
    files = {"file": uploaded_file}
    data = {"email": email, "tipo_factura": tipo_factura_seleccionado}
    response = requests.post(
        "http://127.0.0.1:8000/facturas/completo", files=files, data=data
    )
    if response.status_code == 200:
        st.success("Factura procesada correctamente.")
    else:
        st.error(f"Hubo un error al procesar la factura: {response.text}")
