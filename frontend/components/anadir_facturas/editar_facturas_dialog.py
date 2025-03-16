import streamlit as st


class edit_factura_dialog:
    @st.dialog("Editar Factura")
    def edit_factura_dialog(factura_data):
        factura = factura_data["datos_factura"]

        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            if factura_data.get("url"):
                st.image(factura_data["url"], caption="Factura")

        with col2:
            with st.form("edit_factura_form"):
                st.subheader("Datos Empresa")
                emisor_nombre = st.text_input("Nombre", factura["emisor"]["nombre"])
                emisor_nif = st.text_input("NIF/CIF", factura["emisor"]["NIF_CIF"])
                emisor_domicilio = st.text_input("Domicilio", factura["emisor"]["domicilio"])

                st.subheader("Datos Cliente")
                receptor_nombre = st.text_input("Nombre Cliente", factura["receptor"]["nombre"])
                receptor_nif = st.text_input("NIF/CIF Cliente", factura["receptor"]["NIF_CIF"])
                receptor_domicilio = st.text_input("Domicilio Cliente", factura["receptor"]["domicilio"])

                st.subheader("Datos Factura")
                numero_factura = st.text_input("Número de Factura", factura["numero_factura"])
                fecha_expedicion = st.text_input("Fecha de Expedición", factura["fecha_expedicion"])

                submitted = st.form_submit_button("Guardar")

                if submitted:
                    factura_data["datos_factura"]["emisor"]["nombre"] = emisor_nombre
                    factura_data["datos_factura"]["emisor"]["NIF_CIF"] = emisor_nif
                    factura_data["datos_factura"]["emisor"]["domicilio"] = emisor_domicilio
                    factura_data["datos_factura"]["receptor"]["nombre"] = receptor_nombre
                    factura_data["datos_factura"]["receptor"]["NIF_CIF"] = receptor_nif
                    factura_data["datos_factura"]["receptor"]["domicilio"] = receptor_domicilio
                    factura_data["datos_factura"]["numero_factura"] = numero_factura
                    factura_data["datos_factura"]["fecha_expedicion"] = fecha_expedicion
                    st.success("Factura actualizada con éxito")
