import streamlit as st
import json
import requests
import re
from datetime import datetime

def calcular_total_con_iva(items):
    total = 0
    for item in items:
        total_item = item['cantidad'] * item['precio_unitario']
        iva = total_item * (item['tipo_IVA'] / 100)
        total_item_con_iva = total_item + iva
        total += total_item_con_iva
    return total

def calcular_total_sin_iva(items):
    total = 0
    for item in items:
        total_item = item['cantidad'] * item['precio_unitario']
        total += total_item
    return total

def edit_factura(factura_data):

    def validar_nif_cif(nif):
        return bool(re.match(r'^[A-Z0-9]{8,9}$', nif))

    def validar_fecha(fecha):
        if fecha is None:
            fecha = " "
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validar_campos_factura():
        errores = []

        if not emisor_nombre:
            errores.append("El nombre del emisor no puede estar vacío.")
        if not validar_nif_cif(emisor_nif):
            errores.append("El NIF/CIF del emisor no es válido.")
        if not emisor_domicilio:
            errores.append("El domicilio del emisor no puede estar vacío.")

        if not tipo_factura:
            errores.append("El tipo de factura no puede estar vacío.")
        if not numero_factura:
            errores.append("El número de factura no puede estar vacío.")
        if not serie_factura:
            errores.append("La serie de la factura no puede estar vacía.")
        if not validar_fecha(fecha_expedicion):
            errores.append("La fecha de expedición debe tener el formato YYYY-MM-DD.")
        if not validar_fecha(fecha_operacion):
            errores.append("La fecha de operación debe tener el formato YYYY-MM-DD.")
        if not tipo_factura_seleccionado:
            errores.append("Debe seleccionar operacion de Venta o Compra")

        return errores

    def validar_campos_items(nuevo_nombre, cantidad, precio_unitario):#, tipo_iva, cuota_iva):
        errores = []

        if not nuevo_nombre.strip():
            errores.append("El nombre del producto no puede estar vacío.")

        if not cantidad:
            errores.append("La cantidad no puede estar vacía.")
        else:
            try:
                cantidad_valida = int(cantidad)
                if cantidad_valida <= 0:
                    errores.append("La cantidad debe ser un número entero positivo.")
            except ValueError:
                errores.append("La cantidad debe ser un número entero válido.")

        if not precio_unitario:
            errores.append("El precio unitario no puede estar vacío.")
        else:
            try:
                precio_unitario_valido = float(precio_unitario)
                if precio_unitario_valido <= 0:
                    errores.append("El precio unitario debe ser un número positivo.")
            except ValueError:
                errores.append("El precio unitario debe ser un número válido.")
        #
        # if not tipo_iva.strip():
        #     errores.append("El tipo de IVA no puede estar vacío.")
        # else:
        #     try:
        #         tipo_iva_valido = float(tipo_iva)
        #         if tipo_iva_valido < 0 or tipo_iva_valido > 100:
        #             errores.append("El tipo de IVA debe estar entre 0 y 100.")
        #     except ValueError:
        #         errores.append("El tipo de IVA debe ser un número válido.")
        #
        # if not cuota_iva.strip():
        #     errores.append("La cuota de IVA no puede estar vacía.")
        # else:
        #     try:
        #         cuota_iva_valida = float(cuota_iva)
        #         if cuota_iva_valida < 0:
        #             errores.append("La cuota de IVA no puede ser negativa.")
        #     except ValueError:
        #         errores.append("La cuota de IVA debe ser un número válido.")

        return errores

    def imprimir_errores(errores,flag):
        if flag is not False:
            for error in errores:
                st.error(error)

    @st.dialog("Borrar item", width="small")
    def delete_confirm(item):
        st.write(f"Esta seguro de que quiere borrar {item['descripcion']}?")
        col1_modal, col2_modal = st.columns([1, 1], gap="medium")
        with col1_modal:
            if st.button("Si", use_container_width=True):
                if item in items:
                    items.remove(item)
                st.rerun()
        with col2_modal:
            if st.button("No", use_container_width=True):
                st.rerun()

    factura = factura_data["datos_factura"]
    #Tengo el email y necesito el id para actualizar la factura
    email = st.session_state["email"]
    id = requests.get(f"https://facturia-backend-48606537894.us-central1.run.app/usuarios/{email}").json()

    items = factura["items"]
    imprimir_errores_flag = False
    imprimir_errores_items_flag = False
    errores = ""
    errores_items = ""
    col1_form, col2_form, col3_form = st.columns([1, 1, 1], gap="medium")


    with col1_form:
        image_container = st.container(border=True)
        with image_container:
            st.title("Factura")
            st.image(factura_data["url"], use_container_width=True)
            # total_con_IVA = calcular_total_con_iva(items)
            total_sin_IVA = calcular_total_sin_iva(items)
            st.subheader("Total de la Factura:")
            col1, col22 = st.columns([1, 1], gap="medium")
            tipo_factura_seleccionado = st.radio(
                "Elija el tipo de factura",
                ["Venta", "Compra"],
                key="tipo_factura",
                horizontal=True,
                index=0 if factura_data["tipo_de_factura"] == "Venta" else 1
            )
            st.write(f"Total: €{total_sin_IVA:.2f}", unsafe_allow_html=True)
            # with col1:
            #     st.write(f"Total con IVA: €{total_con_IVA:.2f}", unsafe_allow_html=True)
            # with col22:
            #     st.write(f"Total sin IVA: €{total_sin_IVA:.2f}", unsafe_allow_html=True)

    with col2_form:
        datosfactura_container = st.container(border=True)
        with datosfactura_container:
            st.title("Datos Factura")

            st.subheader("Emisor")
            emisor_nombre = st.text_input("Nombre*", factura["emisor"]["nombre"])
            emisor_nif = st.text_input("NIF/CIF*", factura["emisor"]["NIF_CIF"],max_chars=9)
            emisor_domicilio = st.text_input("Domicilio*", factura["emisor"]["domicilio"])

            st.subheader("Receptor")
            receptor_nombre = st.text_input("Nombre Cliente", factura["receptor"]["nombre"])
            receptor_nif = st.text_input("NIF/CIF Cliente", factura["receptor"]["NIF_CIF"],max_chars=9)
            receptor_domicilio = st.text_input("Domicilio Cliente", factura["receptor"]["domicilio"])

            st.subheader("Datos Factura")
            tipo_factura = st.text_input("Tipo de Factura*", factura["tipo_factura"])
            numero_factura = st.text_input("Número de Factura*", factura["numero_factura"])
            serie_factura = st.text_input("Serie*", factura["serie"])
            fecha_expedicion = st.text_input("Fecha de Expedición (YYYY-MM-DD)*", factura["fecha_expedicion"]  if factura["fecha_expedicion"] else "")
            fecha_operacion = st.text_input("Fecha de Operación (YYYY-MM-DD)*", factura["fecha_operacion"] if factura["fecha_operacion"] else "")

            if st.button("Confirmar datos de la factura"):
                errores = validar_campos_factura()
                if errores:
                    imprimir_errores_flag = True
                else:
                    factura_data["datos_factura"]["tipo_factura"] = tipo_factura
                    factura_data["datos_factura"]["numero_factura"] = numero_factura
                    factura_data["datos_factura"]["serie"] = serie_factura
                    factura_data["datos_factura"]["fecha_expedicion"] = fecha_expedicion
                    factura_data["datos_factura"]["fecha_operacion"] = fecha_operacion
                    factura_data["datos_factura"]["emisor"]["nombre"] = emisor_nombre
                    factura_data["datos_factura"]["emisor"]["NIF_CIF"] = emisor_nif
                    factura_data["datos_factura"]["emisor"]["domicilio"] = emisor_domicilio
                    factura_data["datos_factura"]["receptor"]["nombre"] = receptor_nombre
                    factura_data["datos_factura"]["receptor"]["NIF_CIF"] = receptor_nif
                    factura_data["datos_factura"]["receptor"]["domicilio"] = receptor_domicilio
                    factura_data["datos_factura"]["totales"]["total_con_iva"] = round(total_sin_IVA,2)
                    # factura_data["datos_factura"]["totales"]["total_sin_iva"] = round(total_sin_IVA, 2)
                    factura_data["tipo_de_factura"] = tipo_factura_seleccionado
                    factura_data["id_usuario"] = id
                    factura_data_json = json.dumps(factura_data)

                    response = requests.put(
                        f" https://facturia-backend-48606537894.us-central1.run.app/facturas/actualizacion/{factura_data["id_factura"]}",
                        data={
                            "id_factura": factura_data["id_factura"],
                            "factura": factura_data_json
                        }
                    )
                    if response.status_code == 200:
                        st.session_state["layoutConfig"] = "centered"
                        st.session_state["edit_factura"] = ""
                        st.rerun()

    with col3_form:
        items_container = st.container(border=True)
        with items_container:
            if items:
                st.title("Items Factura")

                selected_index = st.selectbox("Selecciona un item:", range(len(items)),
                                              format_func=lambda i: items[i]["descripcion"])

                selected_item = items[selected_index]

                nuevo_nombre = st.text_input("Nuevo Nombre*", selected_item['descripcion'])
                cantidad = st.number_input("Cantidad*", min_value=1, value=int(selected_item['cantidad']))
                precio_unitario = st.text_input("Precio Unitario*", str(selected_item['precio_unitario']))
                # tipo_iva = st.text_input("Tipo IVA*", str(selected_item['tipo_IVA']))
                # cuota_iva = st.text_input("Cuota IVA*", str(selected_item['cuota_IVA']))

                col1_update, col2_add, col3_delete = st.columns([1, 1, 1], gap="medium")
                with col1_update:
                    if st.button("Actualizar", use_container_width=True):
                        errores_items = validar_campos_items(nuevo_nombre, cantidad, precio_unitario)#, tipo_iva, cuota_iva)
                        if errores_items:
                            imprimir_errores_items_flag = True
                        else:
                            items[selected_index]["descripcion"] = nuevo_nombre
                            items[selected_index]["cantidad"] = cantidad
                            items[selected_index]["precio_unitario"] = round(float(precio_unitario),2)
                            # items[selected_index]["tipo_IVA"] = round(float(tipo_iva),2)
                            # items[selected_index]["cuota_IVA"] = round(float(cuota_iva),2)
                            st.rerun()
                with col2_add:
                    if st.button("Añadir", use_container_width=True):
                        nuevo_item = {
                            "descripcion": "item nuevo",
                            "cantidad": 1,
                            "precio_unitario": 0.0,
                            "tipo_IVA": 0.0,
                            "cuota_IVA": 0.0
                        }
                        items.append(nuevo_item)
                        st.rerun()
                with col3_delete:
                    if st.button("Eliminar", use_container_width=True):
                        delete_confirm(selected_item)

            else:
                st.title("No items found")
                if st.button("Añadir item"):
                    nuevo_item = {
                        "descripcion": "item nuevo",
                        "cantidad": 1,
                        "precio_unitario": 0.0,
                        "tipo_IVA": 0.0,
                        "cuota_IVA": 0.0
                    }
                    items.append(nuevo_item)
                    st.rerun()
    imprimir_errores(errores, imprimir_errores_flag)
    imprimir_errores(errores_items, imprimir_errores_items_flag)


edit_factura(st.session_state.get("edit_factura", {}))
