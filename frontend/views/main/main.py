import streamlit as st
from components.inicio.container_mis_facturas import misfacturasclass
from components.inicio.container_economia import economiaclass


# st.set_page_config(page_title="FacturIA", layout="wide")
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

.sidebar-profile {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
.sidebar-profile img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid white;
}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


economiaclass().render_economia()
misfacturasclass().misfacturas()
