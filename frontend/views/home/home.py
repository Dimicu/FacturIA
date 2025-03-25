import streamlit as st

page_bg_img = """
<style>
*{
color: white}
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    opacity: 0.9;
}
[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0);
    z-index: 9999;
}[data-testid="stHeader"] {
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
h1, p{

    text-align: center;
    font-size: 90px;
    size: 1em;

.footer {
    width: 100%;
    text-align: center;
    padding: 15px;
    font-size: 14px;

}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


st.markdown(
    "<h1>Bienvenido a FacturIA, tu asistente financiero personal</h1>",
    unsafe_allow_html=True,
)
st.divider()
st.markdown(
    "<p>FacturIA es una aplicación que te ayuda a gestionar tus facturas de manera sencilla y rápida.</p>",
    unsafe_allow_html=True,
)
footer = """
<div class="footer">
    <p>© 2025 FacturIA | Creado con ❤️ por  Diego, Jose, Javi y Julián</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
