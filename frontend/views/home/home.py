import streamlit as st

page_bg_img = """
<style>

[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    opacity: 0.9;
}
[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0);
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.5);
}
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}



[data-testid="stToolbar"]{
    right: 2rem;
}
.title {
        text-align: center;
        font-size: 60px;
        color: #0e9987;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    }
    .h1 {
        text-align: center;
        font-size: 20px;
        color: white;
    }
    
</style>
"""

# Aplicar el CSS al documento
st.markdown(page_bg_img, unsafe_allow_html=True)

# Contenido de la aplicación

st.markdown(
    '<h1 class="title">Bienvenido a FacturIA, tu asistente financiero</h1>',
    unsafe_allow_html=True,
)
st.divider()
st.markdown(
    '<p class="text">FacturIA es una aplicación que te ayuda a gestionar tus facturas de manera sencilla y rápida.</p>',
    unsafe_allow_html=True,
)
