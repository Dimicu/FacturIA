import streamlit as st
import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.controller.controller import registro

backend_url = "http://localhost:8000"


def register():
    st.title("Registrarse en FacturIA")

    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    user_data = {"email": email, "password": password}

    if st.button("enviar"):
        response_register = registro(user_data)

        print(response_register)


register()