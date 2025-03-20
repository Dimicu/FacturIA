from datetime import datetime

import streamlit as st
import requests
from streamlit import session_state

st.session_state["actualizar_factura"] = ""

def factura_mini_card(id_factura, numero_factura, emisor, receptor, fecha, total, tipo_factura):
    """Crea una tarjeta de factura mostrando los datos esenciales, incluyendo si es venta o compra"""
    with st.container():
        col1, col2 = st.columns(2)
        nombre = emisor if tipo_factura == "Compra" else receptor

        with col1:
            st.write(f"**Num. Factura:** {numero_factura}")
            st.write(f"**Cliente/Proveedor:** {nombre}")
            st.write(f"**Fecha:** {datetime.strptime(fecha, '%Y-%m-%d').strftime('%d/%m/%Y')}")

        with col2:
            st.write(f"**Tipo:** {tipo_factura.capitalize()}")  # Muestra "Venta" o "Compra"
            st.write(f"**Total:** {total}")





class misfacturasclass:
    def misfacturas(self):
        factura_container = st.container(border=True)
        with factura_container:
            info_row = st.columns(1)
            bill_row = st.columns(1)

            with info_row[0]:
                st.title("Mis facturas")
            with bill_row[0]:

                filtro = st.radio("Filtrar por:", ["Todas", "Venta", "Compra"], horizontal=True)

                with st.spinner('Cargando tus facturas...'):
                    response = requests.get(f"http://127.0.0.1:8000/facturas/{session_state['email']}")
                    datos = response.json()
                    st.write(st.session_state["edit_factura"])

                    if datos["data"] != []:
                        if "data" in datos:
                            facturas_filtradas = [
                                factura for factura in datos["data"]
                                if filtro == "Todas" or factura["tipo_de_factura"].lower() == filtro.lower()
                            ]

                            for factura in facturas_filtradas:
                                with st.container(border=True):
                                    factura_mini_card(
                                        factura["id_factura"],
                                        factura["datos_factura"]["numero_factura"],
                                        factura["datos_factura"]["emisor"]["nombre"],
                                        factura["datos_factura"]["receptor"]["nombre"],
                                        factura["datos_factura"]["fecha_expedicion"],
                                        factura["datos_factura"]["totales"]["total_con_iva"],
                                        factura["tipo_de_factura"]
                                    )
                                    if st.button("Editar", key=f"editar_{factura['id_factura']}"):
                                        st.session_state["layoutConfig"] = "wide"
                                        st.session_state["edit_factura"] = factura
                                        st.rerun()



                        else:
                            st.error("No se encontraron facturas o hubo un error al cargar los datos.")
                    else:
                        st.write("No hay facturas disponibles, prueba a añadir una mediante ´añadir facturas´")

