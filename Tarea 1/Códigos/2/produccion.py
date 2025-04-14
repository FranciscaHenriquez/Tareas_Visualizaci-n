import pandas as pd
import plotly.graph_objects as go

# Leer archivo Excel
file_path = "prod.xlsx"
df = pd.read_excel(file_path)

# Renombrar primera columna como 'Alimento'
df = df.rename(columns={df.columns[0]: 'Alimento'})

# Mantener el orden original de las temporadas
temporadas_ordenadas = df.columns[1:].tolist()

# Derretir el DataFrame (formato largo)
df_long = df.melt(id_vars='Alimento', 
                  var_name='Temporada', 
                  value_name='Producción')

# Asegurar el orden de temporadas como en el Excel
df_long["Temporada"] = pd.Categorical(df_long["Temporada"], 
                                      categories=temporadas_ordenadas, 
                                      ordered=True)

# Eliminar nulos
df_long.dropna(subset=['Producción'], inplace=True)

# Ordenar alimentos por producción total
orden_alimentos = df_long.groupby("Alimento")["Producción"].sum().sort_values().index.tolist()
df_long["Alimento"] = pd.Categorical(df_long["Alimento"], categories=orden_alimentos, ordered=True)
df_long = df_long.sort_values(["Alimento", "Temporada"])

# Crear figura
fig = go.Figure()

# Usar colorescale con buen contraste (Turbo o Viridis)
show_legend = False  # Desactiva leyenda por temporada

for idx, temporada in enumerate(temporadas_ordenadas):
    df_temp = df_long[df_long["Temporada"] == temporada]
    fig.add_trace(go.Bar(
        y=df_temp["Alimento"],
        x=df_temp["Producción"],
        name=temporada,
        orientation='h',
        marker=dict(
            color=df_temp["Producción"],
            colorscale='Turbo',
            cmin=df_long["Producción"].min(),
            cmax=df_long["Producción"].max(),
            colorbar=dict(title="Producción") if idx == 0 else None
        ),
        hovertemplate='Temporada: %{customdata[0]}<br>Producción: %{x}',
        customdata=df_temp[["Temporada"]],
        showlegend=False  # <---- Esto desactiva la leyenda por temporada
    ))


# Layout
fig.update_layout(
    barmode='stack',
    title="Producción de Alimentos por Temporada (Barras Apiladas con Heatmap)",
    xaxis_title="Producción Total",
    yaxis_title="Alimento",
    height=600,
    template="plotly_white"
)

fig.show()

# Al final del script anterior...
fig.write_image("produccionxtemporada.png", width=1200, height=600)