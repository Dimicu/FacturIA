import streamlit as st


def add_bill_button_style(text):
    estilo_boton = """<style>
                .my-bill-button {
                    font-size: 30px;
                    border: none;
                    border-radius: 50%;
                    padding: 0px 15px;
                    margin-top: 20px;
                    float: right;
                    margin-right: 20px;
                    transition: background-color 0.3s ease;
                }
                .my-bill-button:hover {
                    background-color: #dcdde0;
                }
            </style>"""

    button_html = f'''
            {estilo_boton}
            <button class="my-bill-button">{text}</button>
        '''
    return button_html


def factura_card_style():
    style = """
    <style>
        .factura-card {
            border: 2px solid #c4c4c7;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
        }
        .factura-card p {
            font-size: 16px;
            margin: 5px 0;
        }
    </style>
    """
    return style


def factura_card(id, cliente, fecha, total):
    card_html = f"""
    <div class="factura-card">
        <p><strong>ID de Factura:</strong> {id}</p>
        <p><strong>Cliente:</strong> {cliente}</p>
        <p><strong>Fecha:</strong> {fecha}</p>
        <p><strong>Total:</strong> {total} EUR</p>
    </div>
    """
    return card_html

def misfacturas(self):
    factura_container = st.container(border=True)
    with factura_container:
        info_row = st.columns(2)
        bill_row = st.columns(1)

        with info_row[0]:
            st.title("Mis facturas")
        with info_row[1]:
            st.markdown(add_bill_button_style("+"), unsafe_allow_html=True)

            st.markdown("""
                <script>
                    const button = document.querySelector(".my-bill-button");
                    button.addEventListener("click", function() {
                        // Forzar un clic en el botón oculto de Streamlit
                        window.parent.document.querySelector('button[title="Botón oculto"]').click();
                    });
                </script>
                """, unsafe_allow_html=True)

        with bill_row[0]:
            st.markdown(factura_card_style(), unsafe_allow_html=True)
            st.markdown(factura_card("12345", "Cliente A", "2025-02-25", "500"), unsafe_allow_html=True)
            st.markdown(factura_card("12346", "Cliente B", "2025-02-24", "300"), unsafe_allow_html=True)
            st.markdown(factura_card("12347", "Cliente C", "2025-02-23", "700"), unsafe_allow_html=True)


class misfacturasclass:
    def misfacturas(self):
        factura_container = st.container(border=True)
        with factura_container:
            info_row = st.columns(2)
            bill_row = st.columns(1)

            with info_row[0]:
                st.title("Mis facturas")
            with info_row[1]:
                st.markdown(add_bill_button_style("+"), unsafe_allow_html=True)

                st.markdown("""
                    <script>
                        const button = document.querySelector(".my-bill-button");
                        button.addEventListener("click", function() {
                            // Forzar un clic en el botón oculto de Streamlit
                            window.parent.document.querySelector('button[title="Botón oculto"]').click();
                        });
                    </script>
                    """, unsafe_allow_html=True)

            with bill_row[0]:
                st.markdown(factura_card_style(), unsafe_allow_html=True)
                st.markdown(factura_card("12345", "Cliente A", "2025-02-25", "500"), unsafe_allow_html=True)
                st.markdown(factura_card("12346", "Cliente B", "2025-02-24", "300"), unsafe_allow_html=True)
                st.markdown(factura_card("12347", "Cliente C", "2025-02-23", "700"), unsafe_allow_html=True)


# class container:
#     render_misfacturas()