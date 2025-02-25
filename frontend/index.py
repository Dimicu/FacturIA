import streamlit as st
import requests
from pages.login import login_page

# API_URL = "http://127.0.0.1:8000/login"  # Cambiar el puerto si es necesario


def index():
    st.title("Bienvenido a FacturAi")


if __name__ == "__main__":
    index()
    login_page()
