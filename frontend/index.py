# from time import sleep
# from pages.login import login_page
import streamlit as st


st.title("Bienvenidos a FacturIA")

if st.button("Inicia Sesión"):
    st.Page("pages/login.py")


if st.button("Registrar"):
    st.Page("pages/register.py")
