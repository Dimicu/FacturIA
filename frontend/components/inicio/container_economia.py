import plotly.graph_objects as go
import requests
import streamlit as st

page_trans_bg_img_ploty = """<style>
[data-testid="stPlotlyChart"]{
background-color: rgba(0, 0, 0, 0);
}</style>"""
st.markdown(page_trans_bg_img_ploty, unsafe_allow_html=True)


class economiaclass:
    def render_economia(self):
        economia_container = st.container(border=True)
        response = requests.get(
            f"https://facturia-backend-48606537894.us-central1.run.app/facturas/balance/{st.session_state['email']}"
        )
        data = response.json()
        if not data:
            st.warning("⚠️ No se encontraron datos de balance.")
        else:
            with economia_container:

                ingresos = round(data[0]["ingresos_fact"], 2)
                gastos = round(data[0]["gastos_fact"], 2)
                balance = round(data[0]["balance_fact"], 2)
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
                colores = ["#DC3545 ", "#28A745", "#007BFF"]  # Azul, Rojo, Verde

                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=["Gastos", "Ingresos", "Balance"],
                            values=[gastos, ingresos, balance],
                            hole=0.6,  # Tamaño del agujero del donut
                            marker=dict(
                                colors=colores, line=dict(color="#FFFFFF", width=2)
                            ),  # Colores y bordes
                            hoverinfo="label+value",  # Muestra etiqueta y valor en hover
                            textinfo="none",
                        )
                    ]
                )

                # Ajustar diseño del gráfico
                fig.update_layout(
                    height=330,
                    width=330,  # Tamaño del gráfico
                    margin=dict(l=10, r=10, t=10, b=10),  # Márgenes
                    showlegend=False,  # Ocultar leyenda
                    hoverlabel=dict(
                        font_size=14, font_family="Arial"
                    ),  # Tamaño de letra en hover
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                )
                # fig.update_layout(
                #     config={
                #         "displayModeBar": True,
                #     }
                # )

                st.plotly_chart(fig, use_container_width=True)
