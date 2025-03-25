import streamlit as st
import sys
import os
import time
import re
import requests

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
*{
text-align: center;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


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
                    "https://facturia-backend-48606537894.us-central1.run.app/registro",
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
