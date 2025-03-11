import streamlit as st

class economiaclass:
    def render_economia(self):
        economia_container = st.container(border=True)

        with economia_container:
            col1, col2, col3 = st.columns(3, gap="medium")

            # Ingresos en la primera columna
            with col1:
                st.subheader("Ingresos")
                st.write("Aquí se muestran los ingresos")

            # Gastos en la segunda columna
            with col2:
                st.subheader("Gastos")
                st.write("Aquí se muestran los gastos")

            # Resultado en la tercera columna
            with col3:
                st.subheader("Resultado")
                st.write("Aquí se muestra el resultado neto")
