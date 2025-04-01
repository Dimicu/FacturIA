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

                # Solo mostrar el gráfico si hay transacciones
                if ingresos == 0 and gastos == 0:
                    st.info("📊 Añade facturas para ver el análisis gráfico.")
                    return

                # Ajustar colores según el balance
                if balance >= 0:
                    colores = ["#DC3545", "#28A745", "#007BFF"]  # Rojo, Verde, Azul
                    labels = ["Gastos", "Ingresos", "Balance"]
                    values = [gastos, ingresos, balance]
                else:
                    colores = ["#DC3545", "#28A745"]  # Rojo, Verde
                    labels = ["Gastos", "Ingresos"]
                    values = [gastos, ingresos]

                # Calcular rentabilidad (evitar división por cero)
                if gastos > 0:
                    rentabilidad = balance / gastos * 100
                else:
                    rentabilidad = 0
                    if balance > 0:
                        rentabilidad = 100  # Si hay balance positivo pero no gastos

                # Determinar estado y emoji según el balance
                if balance > 0:
                    estado = "😊"
                    color = "#116324"
                elif balance < 0:
                    estado = "😟"
                    color = "#961e2a"
                else:
                    estado = "😐"
                    color = "#0c63c2"

                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=labels,
                            values=values,
                            hole=0.6,  # Tamaño del agujero del donut
                            marker=dict(
                                colors=colores, line=dict(color="#FFFFFF", width=2)
                            ),
                            hoverinfo="label+value+percent",
                            textinfo="value+percent",
                            textposition="outside",
                            texttemplate="<span style='color: #31333F; font-size: 16px'>%{value:,.2f}€<br>%{percent}</span>",
                            showlegend=True,
                            legendgroup="group",
                            name="Balance Financiero",
                        )
                    ]
                )

                # Añadir texto en el centro del donut
                fig.add_annotation(
                    text=f"{estado}<br>Balance<br>{balance:,.2f}€<br><span style='font-size: 14px'>Rentabilidad: {rentabilidad:+.1f}%</span>",
                    x=0.5,
                    y=0.5,
                    font=dict(size=20, color=color),
                    showarrow=False,
                    align="center",
                )

                # Ajustar diseño del gráfico
                fig.update_layout(
                    height=450,  # Aumentado la altura total
                    width=400,
                    margin=dict(
                        l=20, r=120, t=20, b=50
                    ),  # Aumentado el margen inferior
                    showlegend=True,  # Mostrar leyenda
                    legend=dict(
                        orientation="v",  # Leyenda vertical
                        yanchor="middle",  # Anclado al medio
                        y=0.5,  # Centrado verticalmente
                        xanchor="left",  # Anclado a la izquierda de su posición
                        x=1.1,  # Posicionado fuera del gráfico
                        font=dict(size=12),
                        bgcolor="rgba(255, 255, 255, 0.4)",
                        bordercolor="rgba(0, 0, 0, 0.2)",
                        borderwidth=1,
                    ),
                    hoverlabel=dict(font_size=14, font_family="Arial", bgcolor="white"),
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                )

                st.plotly_chart(
                    fig,
                    config={
                        "displayModeBar": False,
                        "displaylogo": False,
                        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                    },
                    use_container_width=True,
                )
