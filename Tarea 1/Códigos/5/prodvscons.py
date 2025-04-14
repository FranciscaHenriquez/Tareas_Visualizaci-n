import pandas as pd
import plotly.graph_objects as go

# Cargar archivo Excel
file_path = "consolidado.xlsx"
df = pd.read_excel(file_path, skiprows=2)

# Renombrar columnas
df = df.rename(columns={
    df.columns[1]: "Año",
    df.columns[2]: "PrecioProductor",
    df.columns[3]: "PrecioConsumidor"
})

# Limpieza
df = df.dropna(subset=["Año", "PrecioProductor", "PrecioConsumidor"])
df["Año"] = df["Año"].astype(int)

# Convertir años a string para usar como etiquetas radiales
categorias = df["Año"].astype(str).tolist()

# Crear gráfico polar
fig = go.Figure()

# Trazo para Precio del Productor
fig.add_trace(go.Scatterpolar(
    r=df["PrecioProductor"],
    theta=categorias,
    mode='lines+markers',
    name='Precio Productor',
    line=dict(color='royalblue')
))

# Trazo para Precio del Consumidor
fig.add_trace(go.Scatterpolar(
    r=df["PrecioConsumidor"],
    theta=categorias,
    mode='lines+markers',
    name='Precio Consumidor',
    line=dict(color='orange')
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, title='Precio (CLP)', tickangle=45)
    ),
    title="Comparación del promedio anual del precio de 1L de leche por parte de un productor y el precio pagado por los consumidores",
    showlegend=True
)

fig.show()

# Al final del script anterior...
fig.write_image("consumidorvsproductor.png", width=1200, height=600)
