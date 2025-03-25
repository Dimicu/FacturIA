import streamlit as st
import requests
import time

page_bg_img = """
<style>


[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    opacity: 0.9;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.5);
    z-index: -1;
}
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0);
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

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
        "https://facturia-backend-48606537894.us-central1.run.app/facturas/file",
        files=files,
        data=data,
    )

    for i in range(1, 101):
        time.sleep(0.02)
        progreso.progress(i)
    if response.status_code == 200:
        st.success("Factura procesada correctamente.")
        progreso.empty()
        mensaje.empty()
        st.session_state["layoutConfig"] = "wide"
        st.session_state["anadir_factura"] = response.json()
        st.session_state["imagen_factura"] = uploaded_file
        st.session_state["venta_compra"] = tipo_factura_seleccionado
        st.rerun()

    else:
        st.error(f"Hubo un error al procesar la factura: {response.text}")
