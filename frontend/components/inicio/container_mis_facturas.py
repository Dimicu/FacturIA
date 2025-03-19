import streamlit as st
import requests
from streamlit import session_state


def factura_card_style():
    style = """
    <style>
        .factura-card {
            border: 2px solid #c4c4c7;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
            cursor: pointer;
            transition: transform 0.2s ease-in-out;
        }
        .factura-card:hover {
            background-color: #f1f1f1;
        }
        .factura-card p {
            font-size: 16px;
            margin: 5px 0;
            color: black; /* Asegura que el texto no sea azul */
        }
        /* Asegura que el enlace no esté subrayado */
        .factura-link {
            text-decoration: none !important;  /* Añadir !important para sobrescribir cualquier otro estilo */
            color: inherit !important;         /* Asegura que el color no sea azul */
            display: block;                    /* Hace que el enlace abarque toda la tarjeta */
        }
    </style>
    """
    return style


def factura_card(id, cliente, fecha, total):
    factura_url = f"/factura_detalle?id={id}"  # URL de destino
    card_html = f"""
    <a href="{factura_url}" class="factura-link">
        <div class="factura-card">
            <p><strong>ID de Factura:</strong> {id}</p>
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Fecha:</strong> {fecha}</p>
            <p><strong>Total:</strong> {total} EUR</p>
        </div>
    </a>
    """
    return card_html


class misfacturasclass:
    def misfacturas(self):
        factura_container = st.container(border=True)
        with factura_container:
            info_row = st.columns(1)
            bill_row = st.columns(1)

            with info_row[0]:
                st.title("Mis facturas")
            with bill_row[0]:
                with st.spinner('Cargando tus facturas...'):
                    st.markdown(factura_card_style(), unsafe_allow_html=True)
                    response = requests.get(f"https://facturia-backend-48606537894.us-central1.run.app/facturas/{session_state['email']}")
                    data = response.json()
                    if data["data"] != []:
                        if "data" in data:
                            for factura in data["data"]:
                                st.markdown(
                                    factura_card(
                                        factura["id_factura"],
                                        factura["datos_factura"]["receptor"]["nombre"],
                                        factura["datos_factura"]["fecha_operacion"],
                                        factura["datos_factura"]["totales"].get("total_factura", "No disponible")
                                    ),
                                    unsafe_allow_html=True
                                )
                        else:
                            st.error("No se encontraron facturas o hubo un error al cargar los datos.")
                    else:
                        st.write("No hay facturas disponibles, prueba a añadir una mediante ´añadir facturas´")

