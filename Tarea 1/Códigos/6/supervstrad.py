import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Leer el archivo Excel
file_path = "variacion.xlsx"
df = pd.read_excel(file_path)
df = df.rename(columns={df.columns[0]: 'Alimento', df.columns[1]: 'Variación'})

# Ordenar de menor a mayor para tener menor arriba
df_sorted = df.sort_values(by="Variación", ascending=True).reset_index(drop=True)
df_sorted["Variación_neg"] = -df_sorted["Variación"]

# Obtener lista de alimentos y colores únicos
alimentos_order = df_sorted['Alimento'].tolist()
n = len(df_sorted)
color_scale = px.colors.qualitative.Set3  # puedes cambiar a Set1, Pastel, etc.
colors = (color_scale * (n // len(color_scale) + 1))[:n]

# Crear figura
fig = go.Figure()

# Agregar barras espejo para cada alimento (lado negativo)
for i, row in df_sorted.iterrows():
    fig.add_trace(go.Bar(
        y=[row['Alimento']],
        x=[-row['Variación']],
        orientation='h',
        marker_color=colors[i],
        showlegend=False,
        hovertemplate=f"{row['Alimento']}<br>Variación: {row['Variación']}%"
    ))

# Agregar barras reales para cada alimento (lado positivo)
for i, row in df_sorted.iterrows():
    fig.add_trace(go.Bar(
        y=[row['Alimento']],
        x=[row['Variación']],
        orientation='h',
        marker_color=colors[i],
        showlegend=False,
        hovertemplate=f"{row['Alimento']}<br>Variación: {row['Variación']}%"
    ))

# Configurar eje X simétrico y ocultar etiquetas negativas
max_val = df_sorted["Variación"].max()
tick_vals = np.linspace(-max_val, max_val, 11)
tick_text = ["" if v < 0 else f"{v:.1f}" for v in tick_vals]

fig.update_xaxes(
    range=[-max_val, max_val],
    tickmode="array",
    tickvals=tick_vals,
    ticktext=tick_text
)

# Línea central
fig.add_shape(
    type="line",
    x0=0, x1=0,
    y0=-0.5, y1=len(alimentos_order)-0.5,
    line=dict(color="black", width=1)
)

# Configuración final
fig.update_yaxes(
    categoryorder="array",
    categoryarray=alimentos_order,
    autorange="reversed"
)

fig.update_layout(
    title="Variación de Precios en Porcentaje (Supermercado con respecto a Canales Tradicionales)",
    xaxis_title="Variación (%)",
    yaxis_title="Alimento",
    barmode='overlay',
    template="plotly_white",
    showlegend=False,
    height=700,
    margin=dict(l=150, r=50)
)

fig.show()
# Al final del script anterior...
fig.write_image("produccionxtemporada.png", width=1200, height=600)