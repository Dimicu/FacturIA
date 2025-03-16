import streamlit as st
import requests
from components.anadir_facturas.editar_facturas_dialog import edit_factura_dialog
import json


flag_button = True
flag_factura = False
flag_image = False
# st.session_state["edit_factura"] = ""

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
if st.button("Confirmar"):#, disabled=flag_button):
    st.session_state["layoutConfig"] = "wide"
    # email = st.session_state.email
    # files = {"file": uploaded_file}
    # data = {"email": email, "tipo_factura": tipo_factura_seleccionado}
    # response = requests.post(
    #     "http://127.0.0.1:8000/facturas/completo", files=files, data=data
    # # )
    # if response.status_code == 200:
    #     st.success("Factura procesada correctamente.")
    # else:
    #     st.error(f"Hubo un error al procesar la factura: {response.text}")
    json_data = '''
    {
      "id_factura": 148,
      "datos_factura": {
        "items": [
          {
            "cantidad": 1,
            "tipo_IVA": 4,
            "cuota_IVA": 0.0652,
            "descripcion": "FRESON 1",
            "precio_unitario": 1.63
          },
          {
            "cantidad": 2,
            "tipo_IVA": 10,
            "cuota_IVA": 0.21,
            "descripcion": "MANZANAS",
            "precio_unitario": 2.00
          },
          {
            "cantidad": 3,
            "tipo_IVA": 21,
            "cuota_IVA": 0.42,
            "descripcion": "PLATANOS",
            "precio_unitario": 1.50
          }
        ],
        "serie": "200",
        "emisor": {
          "nombre": "SUN FRUIT SPAIN, SL",
          "NIF_CIF": "536982973",
          "domicilio": ""
        },
        "totales": {},
        "receptor": {
          "nombre": "",
          "NIF_CIF": "",
          "domicilio": ""
        },
        "tipo_factura": "Simplificada",
        "numero_factura": "2500?200-000326i8",
        "fecha_operacion": null,
        "fecha_expedicion": "2023-02-13",
        "factura_rectificada": "",
        "menciones_especiales": []
      },
      "nombre_imagen": "d07d2850-c3dc-47a6-b61b-1273d383e233_IMG-20250220-WA0006.jpg",
      "url": "https://kpodogazzevlldfjbmeq.supabase.co/storage/v1/object/sign/imagenes_facturas/d07d2850-c3dc-47a6-b61b-1273d383e233_IMG-20250220-WA0006.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJpbWFnZW5lc19mYWN0dXJhcy9kMDdkMjg1MC1jM2RjLTQ3YTYtYjYxYi0xMjczZDM4M2UyMzNfSU1HLTIwMjUwMjIwLVdBMDAwNi5qcGciLCJpYXQiOjE3NDE4OTMxMDYsImV4cCI6MTc0MTkyMTkwNn0.J1waZ9o3fUa4h7gJ94p1WSqU_53N9YYqFDptKm03zOM"
    }
    '''

    data = json.loads(json_data)
    st.session_state["edit_factura"] = data
    st.rerun()