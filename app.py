import streamlit as st
import pandas as pd
import math
import plotly.express as px

def calcular_margen(presupuesto, recursos, n_semanas):
    costo_total_mensual = recursos['Costo Mensual'].sum()
    if costo_total_mensual == 0 | presupuesto == 0:
        return "N/A"
    margen_estimado = 100 * (presupuesto - costo_total_mensual * n_semanas / 4) / presupuesto
    return round(margen_estimado, 0)

st.title("Calculadora Comercial")

col1, col2, col3 = st.columns(3)

# Parámetros input

presupuesto = col1.number_input("Presupuesto (USD)", min_value=0, value=32000, step=1000)

semanas = col2.number_input("Semanas", min_value=0, value = 4, step = 1)

tipo_cambio = col3.number_input("Tipo de cambio", min_value = 1.0, value = 20.0, step = 0.5)

col4, col5 = st.columns([3,1])

# Tabla de recursos
col4.subheader("Configuración de Recursos")
recursos_df = col4.data_editor(
    pd.DataFrame({
        "Recurso": ["Data Scientist", "Cloud Architect", "QA", "Data Engineer"],
        "Num": [1, 1, 1, 1],
        "Costo Mensual (USD)": [4015, 7812, 1602, 2676]
    }),
    num_rows="dynamic",
    use_container_width=True
)

# Cálculo de costos
recursos_df["Costo Mensual"] = recursos_df["Num"] * recursos_df["Costo Mensual (USD)"]

col5.subheader("Margen estimado")
col5.write(f"## {calcular_margen(presupuesto, recursos_df, semanas)} %")

tiempos = list(map(sum, zip([semanas] * 11, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])))
margenes = []
for i in tiempos:
    margenes.append(calcular_margen(presupuesto, recursos_df, i))

fig = px.line(x=tiempos, y=margenes, labels = {"x":"Semanas", "y":"Margen"}, markers = True)
fig.add_hline(y = 0, line_dash = "dash", line_color = "red", line_width = 2)

st.subheader("Gráfico de Margen vs Semanas")

st.plotly_chart(fig)