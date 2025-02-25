import streamlit as st
from streamlit import title

st.set_page_config(page_title="FacturIA")

def side_bar_button_style(text):
    EstiloBoton = """<style>
                .my-sidebar-button {
                    background-color: #F0F2F6;
                    color: black;
                    text-align: left;
                    font-size: 16px;
                    border: none;
                    border-radius: 8px;
                    width: 100%;
                    transition: background-color 0.3s ease;
                }
                .my-sidebar-button:hover {
                    background-color: #dcdde0;  /* Cambio de color al pasar el ratón */
                }
            </style>"""
    button_html = f'''
            {EstiloBoton}
            <button class="my-sidebar-button">{text}</button>
        '''
    return button_html
def side_bar_user_style(username):
    EstiloSideBarUser = f"""<style>
            .sidebar-title {{
                text-align: left;
                font-size: calc(44px - {len(username) * 0.5}px);
                font-weight: bold;
                margin-bottom: 20px;
                word-wrap: break-word;
                transition: font-size 0.3s ease;
            }}
        </style>"""
    sidebar_title_html = f'''
        {EstiloSideBarUser}
        <div class="sidebar-title">{username}</div>
    '''
    return sidebar_title_html
def add_bill_button_style(text):
    EstiloBoton = """<style>
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
            {EstiloBoton}
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
            margin-top: 20px; 
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

user = "USUARIO"
user_picture = "https://imgs.search.brave.com/JAHeWxUYEwHB7KV6V1IbI9oL7wxJwIQ4Sbp8dHQL09A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMjAx/MzkxNTc2NC9waG90/by91c2VyLWljb24t/aW4tZmxhdC1zdHls/ZS5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9UEotMnZvUWZh/Q3hhZUNsdzZYYlVz/QkNaT3NTTjlIVWVC/SUg1Qk82VmRScz0"

sidebar = st.sidebar
economia_container = st.container(border=True)
factura_container = st.container(border=True)

with sidebar:
    col1, col2 = st.columns(2)
    col1.image(user_picture, width = 150)
    col2.markdown(side_bar_user_style(user), unsafe_allow_html=True)
    st.divider()
    st.markdown(side_bar_button_style("Mi espacio"), unsafe_allow_html=True)

with economia_container:
    col1, col2, col3 = st.columns(3,gap="medium")

    # Ingresos en la primera columna
    with col1:
        st.subheader("Ingresos")
        st.write("Aquí se muestran los ingresos")

    # Gastos en la segunda columna
    with col2:
        st.subheader("Gastos")
        st.write("Aquí se muestran los gastos")

    # Resultado en la tercera columna
    with col3:
        st.subheader("Resultado")
        st.write("Aquí se muestra el resultado neto")
with factura_container:
    infoRow = st.columns(2)
    billRow = st.columns(1)
    with infoRow[0]:
        st.title("Mis facturas")
    with infoRow[1]:
        st.markdown(add_bill_button_style("+"), unsafe_allow_html=True)
    with billRow[0]:
        st.markdown(factura_card_style(), unsafe_allow_html=True)
        st.markdown(factura_card("12345", "Cliente A", "2025-02-25", "500"), unsafe_allow_html=True)
        st.markdown(factura_card("12346", "Cliente B", "2025-02-24", "300"), unsafe_allow_html=True)
        st.markdown(factura_card("12347", "Cliente C", "2025-02-23", "700"), unsafe_allow_html=True)
