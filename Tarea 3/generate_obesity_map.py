import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import numpy as np

data_file_path = "bmi_2016_both_sexes.csv" # ruta

try:
    # carga de los datos
    data_for_map = pd.read_csv(data_file_path)
    
    # data es en % de obesidad
    if 'BMI_BothSexes_2016' in data_for_map.columns:
        data_for_map.rename(columns={'BMI_BothSexes_2016': 'Obesity_Percentage_2016'}, inplace=True)
    elif 'Obesity_Percentage_2016' not in data_for_map.columns:
        if 'Obesity_Percentage_2016' not in data_for_map.columns:
             raise ValueError("La columna de datos esperada ('BMI_BothSexes_2016' o 'Obesity_Percentage_2016') no se encuentra en el archivo.")

except FileNotFoundError:
    print(f"Error: El archivo de datos '{data_file_path}' no fue encontrado.")
    print("Por favor, asegúrate de que el archivo 'bmi_2016_both_sexes.csv' exista y esté accesible.")
    exit() # si el archivo de datos no se encuentra
except ValueError as ve:
    print(str(ve))
    exit()


print("Datos para el mapa cargados (primeras 5 filas):")
print(data_for_map[['Country', 'Obesity_Percentage_2016']].head())

# carga de datos geográficos del mundo

try:
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
except Exception as e:
    print(f"Error al cargar los datos geográficos de 'naturalearth_lowres': {e}")
    print("Asegúrate de tener geopandas y sus dependencias correctamente instaladas.")
    exit()

# corregir nombres de países
world_to_merge = world.copy()

world_name_corrections = {
    "United States of America": "United States",
    "Dem. Rep. Congo": "Democratic Republic of the Congo",
    "Dominican Rep.": "Dominican Republic",
    "Central African Rep.": "Central African Republic",
    "Solomon Is.": "Solomon Islands",
    "Eq. Guinea": "Equatorial Guinea",
    "Bosnia and Herz.": "Bosnia and Herzegovina",
    "S. Sudan": "South Sudan",
    "Côte d'Ivoire": "Cote d'Ivoire",
    "Czechia": "Czech Republic",
    "N. Cyprus": "Cyprus", 
    "eSwatini": "Eswatini", 
    "Timor-Leste": "East Timor"
}
world_to_merge['name_corrected'] = world_to_merge['name'].replace(world_name_corrections)

# fusión de datos geográficos con datos de obesidad
# left para mantener todos los países del mapa base
merged_data = world_to_merge.merge(data_for_map, left_on='name_corrected', right_on='Country', how='left')

expected_matches_threshold = 0.7 * len(data_for_map.dropna(subset=['Obesity_Percentage_2016']))
if merged_data['Obesity_Percentage_2016'].notna().sum() < expected_matches_threshold:
    print("Tasa de coincidencia baja con nombres corregidos. Intentando con nombres originales del mapa...")
    merged_data_orig_name = world.merge(data_for_map, left_on='name', right_on='Country', how='left')
    # si esta segunda fusión da más resultados, se usa
    if merged_data_orig_name['Obesity_Percentage_2016'].notna().sum() > merged_data['Obesity_Percentage_2016'].notna().sum():
        merged_data = merged_data_orig_name
        print(f"Usando fusión con 'world.name' original. Coincidencias: {merged_data['Obesity_Percentage_2016'].notna().sum()}")

final_merged_data = merged_data.copy()

# creacion de mapa coroplético
fig, ax = plt.subplots(1, 1, figsize=(20, 12))

final_merged_data.plot(column='Obesity_Percentage_2016',
                       ax=ax,
                       legend=True,
                       cmap='OrRd',
                       missing_kwds={ # países sin datos
                           "color": "lightgrey",
                           "edgecolor": "grey",
                           "hatch": "..",
                           "label": "Sin Datos de Obesidad / No Mapeado", 
                       },
                       legend_kwds={ 
                           'label': "Porcentaje de Obesidad (Ambos Sexos, 2016)", 
                           'orientation': "horizontal",
                           'shrink': 0.7, 
                           'pad': 0.02, 
                           'aspect': 30 
                           }
                       )

ax.set_title('Porcentaje de Obesidad Global (Ambos Sexos) en 2016', fontdict={'fontsize': 20, 'fontweight' : 'bold'}) 
ax.set_axis_off() 
plt.tight_layout(pad=0.5) 

# guardar la visualización
output_map_filename = "obesidad_porcentaje_2016_mapa_es.png"
try:
    plt.savefig(output_map_filename, dpi=300) 
    print(f"\nMapa guardado exitosamente como: {output_map_filename}")
except Exception as e:
    print(f"Error al guardar el mapa: {e}")

print(f"\nNúmero de países/regiones en el mapa con datos: {final_merged_data['Obesity_Percentage_2016'].notna().sum()}")
print(f"Total de países/regiones en el mapa base: {len(final_merged_data)}")