import json

import streamlit as st
import requests


class economiaclass:
    def render_economia(self):
        economia_container = st.container(border=True)
        response = requests.get(f"http://127.0.0.1:8000/facturas/balance/{st.session_state['email']}")
        data = response.json()
        if not data:
            st.warning("⚠️ No se encontraron datos de balance.")
        else:
            with economia_container:
                col1, col2, col3 = st.columns(3, gap="medium")

                # Ingresos en la primera columna
                with col1:
                    st.subheader("Ingresos")
                    st.write(data[0]["ingresos_fact"])

                # Gastos en la segunda columna
                with col2:
                    st.subheader("Gastos")
                    st.write(data[0]["gastos_fact"])

                # Resultado en la tercera columna
                with col3:
                    st.subheader("Resultado")
                    st.write(data[0]["balance_fact"])

