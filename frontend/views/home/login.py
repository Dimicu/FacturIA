import streamlit as st
import sys
import os
import time
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def login_page():
    st.title("Iniciar sesión en FacturIA")

    if st.session_state.get("logged_in", False):
        st.session_state.authenticated = True
        st.rerun()
        # st.success(f"Ya has iniciado sesión como {st.session_state['email']}")
        # st.button("Crear factura")
        # st.button("Actualizar factura")

        # if st.button("Cerrar sesión"):
        #     st.session_state["logged_in"] = False
        #     st.session_state["email"] = ""
        #     st.rerun()
        # return

    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):

        if not email or not password:
            st.warning("Por favor, ingresa tu correo y contraseña.")
        else:
            user_data = {"email": email, "password": password}

            response = requests.post(
                "https://facturia-backend-48606537894.us-central1.run.app/login", json=user_data
            ).json()

            error_message = ""
            status_code = 0

            try:

                error_message = response.get("error", "")
                status_code = response.get("status_code", 0)

                print("status_code:", status_code)

            except Exception as e:
                st.error("Hubo un error al procesar la respuesta.")

            if status_code == 200:
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.success(f"Bienvenido, {email}")
                st.write("Iniciando aplicación...")
                time.sleep(3)
                st.rerun()

            elif status_code == 400:
                st.error(f"Error: {error_message}")
            # elif status_code == 0:
            #     st.warning("Por favor, ingresa tu correo y contraseña.")
            # # elif status_code == 404:
            # #     st.error(f"Error: {error_message}")
            # #     st.button("Registrarse")
            # #
            # #     response_register = registro(user_data)
            # #     print(response_register)

            else:
                st.error(f"Error desconocido: {error_message}")


login_page()
