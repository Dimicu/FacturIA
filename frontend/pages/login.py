import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from controller.controller import login


def login_page():
    st.title("Iniciar sesión en FacturIA")

    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):

        if not email or not password:
            st.warning("Por favor, ingresa tu correo y contraseña.")
        else:
            user_data = {"email": email, "password": password}

            response = login(user_data)

            error_message = ""
            status_code = 0

            try:

                error_message = response.get("error", "")
                status_code = response.get("status_code", 0)

                print("status_code:", status_code)

            except Exception as e:
                st.error("Hubo un error al procesar la respuesta.")

            if status_code == 200:
                st.success(f"Bienvenido, {email}")
            elif status_code == 400:
                st.error(f"Error: {error_message}")
            elif status_code == 404:
                st.error(f"Error: {error_message}")
            else:
                st.error(f"Error desconocido: {error_message}")
