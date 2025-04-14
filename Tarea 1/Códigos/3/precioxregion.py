import pandas as pd
import plotly.graph_objects as go

# Leer el archivo Excel (ajusta la ruta según corresponda)
file_path = "consolidado.xlsx"
df = pd.read_excel(file_path)

# Renombrar la primera columna a "Alimento" (si aún no lo está)
df = df.rename(columns={df.columns[0]: "Alimento"})

# Obtener la lista de regiones (se asume que son las columnas 2 en adelante)
regiones = df.columns[1:].tolist()

# Opcional: Definir un rango global para la escala radial basado en todo el dataset
min_val = df.iloc[:, 1:].min().min()
max_val = df.iloc[:, 1:].max().max()

# Iterar sobre cada alimento y generar un gráfico de radar individual
for idx, row in df.iterrows():
    alimento = row["Alimento"]
    # Extraer los precios (convierte a lista)
    precios = row[1:].values.tolist()

    # Generar figura radar
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=precios,
        theta=regiones,
        fill='toself',
        name=alimento,
        marker=dict(color='royalblue')
    ))
    
    # Ajustar el layout, fijando el mismo rango radial para todos los gráficos (opcional)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[min_val, max_val]
            )
        ),
        title=f"Precio de {alimento} por Región",
        showlegend=False
    )
    
    # Mostrar el gráfico (en un entorno interactivo se abrirá cada gráfico)
    fig.show()
    
    # Si deseas guardar cada gráfico en HTML, descomenta la siguiente línea:
    # fig.write_html(f"Radar_{alimento.replace(' ', '_')}.html")
    fig.write_image(f"Precio_{alimento.replace(' ','_')}.png", width=1200, height=600)
