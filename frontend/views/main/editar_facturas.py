from time import sleep
import streamlit as st
from itertools import zip_longest
import json


def edit_factura_dialog(factura_data):
    factura = factura_data["datos_factura"]
    items = factura_data["datos_factura"]["items"]

    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    with col1:
        image_container = st.container(border=True)
        with image_container:
            st.title("Factura")
            st.image(factura_data["url"], caption="Factura", use_container_width=True)
    with col2:
        datosfactura_container = st.container(border=True)
        with datosfactura_container:
            st.title("Datos Factura")
            st.subheader("Emisor")
            emisor_nombre = st.text_input("Nombre", factura["emisor"]["nombre"])
            emisor_nif = st.text_input("NIF/CIF", factura["emisor"]["NIF_CIF"])
            emisor_domicilio = st.text_input("Domicilio", factura["emisor"]["domicilio"])

            st.subheader("Receptor")
            receptor_nombre = st.text_input("Nombre Cliente", factura["receptor"]["nombre"])
            receptor_nif = st.text_input("NIF/CIF Cliente", factura["receptor"]["NIF_CIF"])
            receptor_domicilio = st.text_input("Domicilio Cliente", factura["receptor"]["domicilio"])

            st.subheader("Datos Factura")
            numero_factura = st.text_input("Número de Factura", factura["numero_factura"])
            fecha_expedicion = st.text_input("Fecha de Expedición", factura["fecha_expedicion"])
            if st.button("Confirmar datos de la factura"):
                factura_data["datos_factura"]["emisor"]["nombre"] = emisor_nombre
                factura_data["datos_factura"]["emisor"]["NIF_CIF"] = emisor_nif
                factura_data["datos_factura"]["emisor"]["domicilio"] = emisor_domicilio
                factura_data["datos_factura"]["receptor"]["nombre"] = receptor_nombre
                factura_data["datos_factura"]["receptor"]["NIF_CIF"] = receptor_nif
                factura_data["datos_factura"]["receptor"]["domicilio"] = receptor_domicilio
                factura_data["datos_factura"]["numero_factura"] = numero_factura
                factura_data["datos_factura"]["fecha_expedicion"] = fecha_expedicion
                st.session_state["layoutConfig"] = "centered"

        with col3:
            items_container = st.container(border=True)
            with items_container:
                st.title("Items Factura")

                item_descriptions = [item["descripcion"] for item in items]

                selected_item_desc = st.selectbox("Selecciona un item:", item_descriptions)

                selected_item = next(item for item in items if item["descripcion"] == selected_item_desc)

                cantidad = st.text_input("Cantidad", selected_item['cantidad'])
                tipo_iva = st.text_input("Tipo IVA", selected_item['tipo_IVA'])
                cuota_iva = st.text_input("Cuota IVA", selected_item['cuota_IVA'])
                precio_unitario = st.text_input("Precio Unitario", selected_item['precio_unitario'])

                if st.button("Actualizar Objeto"):
                    for item in factura_data["datos_factura"]["items"]:
                        if item["descripcion"] == selected_item_desc:
                            item["cantidad"] = int(cantidad)
                            item["tipo_IVA"] = float(tipo_iva)
                            item["cuota_IVA"] = float(cuota_iva)
                            item["precio_unitario"] = float(precio_unitario)

edit_factura_dialog(st.session_state["edit_factura"])
