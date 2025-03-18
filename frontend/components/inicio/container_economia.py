import plotly.graph_objects as go
import requests
import streamlit as st


class economiaclass:
    def render_economia(self):
        economia_container = st.container(border=True)
        response = requests.get(f"http://127.0.0.1:8000/facturas/balance/{st.session_state['email']}")
        data = response.json()
        if not data:
            st.warning("⚠️ No se encontraron datos de balance.")
        else:
            with economia_container:

                ingresos = data[0]["ingresos_fact"]
                gastos = data[0]["gastos_fact"]
                balance = data[0]["balance_fact"]
                # Primera fila con métricas
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(label="Ingresos", value=f"{ingresos}€")
                with col2:
                    st.metric(label="Gastos", value=f"{gastos}€")
                with col3:
                    st.metric(label="Balance", value=f"{balance}€")

                # Segunda fila con gráfico Donut
                st.divider()  # Línea separadora opcional
                colores = ['#28A745', '#DC3545', '#007BFF']  # Azul, Rojo, Verde

                fig = go.Figure(data=[go.Pie(
                labels=['Ingresos', 'Gastos', 'Balance'],
                values=[ingresos, gastos,balance ],
                hole=0.6,  # Tamaño del agujero del donut
                marker=dict(colors=colores, line=dict(color='#FFFFFF', width=2)),  # Colores y bordes
                hoverinfo="label+value",  # Muestra etiqueta y valor en hover
                textinfo="none",
                textfont=dict(size=14, color="black"),  # Tamaño de texto dentro del gráfico
                outsidetextfont=dict(size=14, color="black")  # Texto fuera del gráfico
            )])

                # Ajustar diseño del gráfico
                fig.update_layout(
                    height=330, width=330,  # Tamaño del gráfico
                    margin=dict(l=10, r=10, t=10, b=10),  # Márgenes
                    showlegend=True,  # Ocultar leyenda
                    hoverlabel=dict(font_size=14, font_family="Arial")  # Tamaño de letra en hover
                )

                st.plotly_chart(fig, use_container_width=True)

