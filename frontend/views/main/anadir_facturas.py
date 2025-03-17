import streamlit as st
import requests
import time

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
if st.session_state.tipo_factura != None:
    flag_factura = True
    tipo_factura_seleccionado = st.session_state.tipo_factura


uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    flag_image = True
    st.image(uploaded_file, caption="imagen_factura")

if flag_image == True and flag_factura == True:
    flag_button = False

if st.button("Confirmar", disabled=flag_button):
    progreso = st.progress(10)
    mensaje = st.empty()
    mensaje.write("FacturIA subiendo y procesando la factura...")

    email = st.session_state.email

    files = {"file": uploaded_file}
    data = {"email": email, "tipo_factura": tipo_factura_seleccionado}
    response = requests.post(
        "http://127.0.0.1:8000/facturas/file", files=files, data=data
    )

    for i in range(1, 101):
        time.sleep(0.02)
        progreso.progress(i)
    if response.status_code == 200:
        st.success("Factura procesada correctamente.")
        progreso.empty()
        mensaje.empty()
        st.session_state["layoutConfig"] = "wide"
        st.session_state["edit_factura"] = response.json()
        st.session_state["imagen_factura"] = uploaded_file
        st.session_state["venta_compra"] = tipo_factura_seleccionado
        st.rerun()

    else:
        st.error(f"Hubo un error al procesar la factura: {response.text}")

