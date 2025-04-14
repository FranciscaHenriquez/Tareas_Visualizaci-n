import pandas as pd
import plotly.express as px

# Leer Excel
file_path = "prod202324.xlsx"
df = pd.read_excel(file_path)

# Renombrar columna A como "Región" si no está nombrada
df = df.rename(columns={df.columns[0]: 'Región'})

# Convertir a formato largo
df_long = df.melt(id_vars='Región', var_name='Alimento', value_name='Producción')

# Crear Heatmap
fig = px.density_heatmap(
    df_long,
    x='Alimento',
    y='Región',
    z='Producción',
    color_continuous_scale='Turbo',
    title="Producción de Alimentos por Región (Heatmap)",
    labels={'Producción': 'Producción'},
)

fig.update_layout(
    xaxis_title="Alimento",
    yaxis_title="Región",
    template="plotly_white",
    height=600
)

fig.show()
# Al final del script anterior...
fig.write_image("produccionxtemporada.png", width=1200, height=600)