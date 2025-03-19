import streamlit as st
import json
import requests


def calcular_total(items):
    total = 0
    for item in items:
        total_item = item['cantidad'] * item['precio_unitario']
        iva = total_item * (item['tipo_IVA'] / 100)
        total_item_con_iva = total_item + iva
        total += total_item_con_iva
    return total


def edit_factura(factura_data, factura_img, venta_compra):
    factura = factura_data
    items = factura_data["items"]

    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    with col1:
        image_container = st.container(border=True)
        with image_container:
            st.title("Factura")
            st.image(factura_img, use_container_width=True)
            total = calcular_total(items)
            st.subheader("Total de la Factura:")
            st.write(f"Total: €{total:.2f}", unsafe_allow_html=True)
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
            tipo_factura = st.text_input("Tipo de Factura", factura["tipo_factura"])
            numero_factura = st.text_input("Número de Factura", factura["numero_factura"])
            serie_factura = st.text_input("Serie", factura["serie"])
            fecha_expedicion = st.text_input("Fecha de Expedición", factura["fecha_expedicion"])
            fecha_operacion = st.text_input("Fecha de Operación",
                                            factura["fecha_operacion"] if factura["fecha_operacion"] else "")

            if st.button("Confirmar datos de la factura"):
                factura_data["tipo_factura"] = tipo_factura
                factura_data["numero_factura"] = numero_factura
                factura_data["serie"] = serie_factura
                factura_data["fecha_expedicion"] = fecha_expedicion
                factura_data["fecha_operacion"] = fecha_operacion
                factura_data["emisor"]["nombre"] = emisor_nombre
                factura_data["emisor"]["NIF_CIF"] = emisor_nif
                factura_data["emisor"]["domicilio"] = emisor_domicilio
                factura_data["receptor"]["nombre"] = receptor_nombre
                factura_data["receptor"]["NIF_CIF"] = receptor_nif
                factura_data["receptor"]["domicilio"] = receptor_domicilio
                factura_data["total"] = total

                factura_data_json = json.dumps(factura_data)

                response = requests.post(
                    "https://facturia-backend-48606537894.us-central1.run.app/facturas/completa",
                    data={
                        "email": st.session_state["email"],
                        "tipo_factura": venta_compra,
                        "json_front_modified": factura_data_json,
                    },
                    files={"file": factura_img},
                )

                if response.status_code == 200:
                    st.session_state["layoutConfig"] = "centered"
                    st.session_state["edit_factura"] = ""
                    st.session_state["imagen_factura"] = ""
                    st.rerun()

    with col3:
        items_container = st.container(border=True)
        if items is not []:
            with items_container:
                    st.title("Items Factura")

                    item_descriptions = [item["descripcion"] for item in items]
                    selected_item_desc = st.selectbox("Selecciona un item:", item_descriptions)
                    selected_item = next(item for item in items if item["descripcion"] == selected_item_desc)

                    cantidad = st.text_input("Cantidad", str(selected_item['cantidad']))
                    precio_unitario = st.text_input("Precio Unitario", str(selected_item['precio_unitario']))
                    tipo_iva = st.text_input("Tipo IVA", str(selected_item['tipo_IVA']))
                    cuota_iva = st.text_input("Cuota IVA", str(selected_item['cuota_IVA']))

                    if st.button("Actualizar Item"):
                        for item in factura_data["items"]:
                            if item["descripcion"] == selected_item_desc:
                                item["cantidad"] = float(cantidad)
                                item["precio_unitario"] = float(precio_unitario)
                                item["tipo_IVA"] = float(tipo_iva)
                                item["cuota_IVA"] = float(cuota_iva)
        else:
            with items_container:
                st.title("No items found")


edit_factura(st.session_state.get("edit_factura", {}), st.session_state.get("imagen_factura", ""), st.session_state["venta_compra"])
