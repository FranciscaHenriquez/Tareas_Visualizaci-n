import pandas as pd
import numpy as np
import plotly.express as px

# Cargar el archivo Excel
file_path = "1 Precio alimentos chile historico.xlsx"
xls = pd.ExcelFile(file_path)
df = xls.parse(xls.sheet_names[0], header=1)

# Extraer nombre del producto
producto = df.loc[1, 'Unnamed: 1'].strip()

# Extraer fechas y valores
fechas = df.iloc[0, 2:].values
valores = df.iloc[1, 2:].values.astype(float)

# Crear DataFrame limpio
bubble_df = pd.DataFrame({
    'Fecha': pd.to_datetime(fechas),
    'Producto': producto,
    'Valor': valores
})


# 2. Transformación logarítmica
bubble_df['TamanoLog'] = np.log1p(bubble_df['Valor'] - bubble_df['Valor'].min())


# Gráfico con transformación logarítmica
fig_log = px.scatter(
    bubble_df,
    x='Fecha',
    y='Producto',
    size='TamanoLog',
    color='Producto',
    hover_data={'Fecha': True, 'Valor': True},
    title='Valores de alimentos históricos representados mediante el valor del índice IPC',
    labels={'Fecha': 'Fecha', 'Producto': 'Producto', 'Valor': 'Índice'},
    size_max=60
)
fig_log.show()

# Al final del script anterior...
fig_log.write_image("bubble_timeline_logaritmico.png", width=1200, height=600)
