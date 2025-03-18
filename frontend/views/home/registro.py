import streamlit as st
import sys
import os
import time
import re
import requests


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def validar_email(email: str) -> bool:
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email) is not None


def register_page():

    st.title("Registrarse en FacturIA")

    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar contraseña", type="password")

    if st.button("Registrar"):
        if not email or not password:
            st.warning("Por favor, ingresa tu correo y contraseña.")
        elif password != confirm_password:
            st.warning("Las contraseñas no coinciden.")
        elif not validar_email(email):
            st.warning("Por favor, ingresa un correo electrónico válido.")
        else:
            user_data = {"email": email, "password": password}

            error_message = ""
            status_code = 0

            try:
                response_register = requests.post(
                    "http://127.0.0.1:8000/registro",
                    json=user_data,
                ).json()

                error_message = response_register["error"]
                status_code = response_register["status_code"]

                print("status_code:", status_code)
                print("Mensaje del frontend:", error_message)

            except Exception as e:
                st.error("Hubo un error al procesar la respuesta.")

            if status_code == 201:
                st.success({error_message})
                st.session_state["logged_in"] = True
                st.session_state.authenticated = True
                st.session_state["email"] = email
                st.write("Redirigiendo...")
                time.sleep(3)
                st.rerun()

            elif status_code == 400:
                st.error(f"Error frontend: {error_message}")
            elif status_code == 409:
                st.error(f"Error frontend: {error_message}")
            else:
                st.error(f"Error desconocido frontend: {error_message}")


register_page()
