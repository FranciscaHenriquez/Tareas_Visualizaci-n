import pandas as pd
from itertools import combinations

try:
    df = pd.read_csv('horaDelTe.csv', sep=';', encoding='latin-1')
except FileNotFoundError:
    print("Asegúrate de que el archivo 'horaDelTe.csv' se encuentra en el directorio correcto.")
    exit()

# reemplazar si por 1 y no por 0
df_numeric = df.replace({'Si': 1, 'No': 0})

# nombre de los productos
products = df.columns.tolist()

#************* pregunta 1 **************

# contar las ventas x producto
product_sales = df_numeric.sum().sort_values(ascending=False)

print("Ventas por producto:")
print(product_sales)

# verificar si pan es el mas vendido
is_pan_top_seller = product_sales.index[0] == 'Pan'
print(f"\n¿Es el Pan el producto más vendido? {is_pan_top_seller}")

#************* pregunta 2 **************

# compras que incluyen pan
pan_purchases = df_numeric[df_numeric['Pan'] == 1]

# contar venta de otros productos cuando se compra pan
co_purchases_with_pan = pan_purchases.drop('Pan', axis=1).sum().sort_values(ascending=False)

print("Productos comprados junto con el Pan:")
print(co_purchases_with_pan)

most_common_with_pan = co_purchases_with_pan.index[0]
print(f"\nEl producto que más tiende a comprarse con Pan es: {most_common_with_pan}")

#************* pregunta 3 **************

# analizar combinaciones de 2 y 3 productos
all_combinations = {}
for n in [2, 3]:
    for combo in combinations(products, n):
        all_combinations[combo] = df_numeric.T.loc[list(combo)].all().sum()

# separar combinaciones con y sin pan
combos_with_pan = {k: v for k, v in all_combinations.items() if 'Pan' in k}
combos_without_pan = {k: v for k, v in all_combinations.items() if 'Pan' not in k}

# ordenar de mayor a menor frecuencia
sorted_combos_with_pan = sorted(combos_with_pan.items(), key=lambda item: item[1], reverse=True)
sorted_combos_without_pan = sorted(combos_without_pan.items(), key=lambda item: item[1], reverse=True)

print("Combinación SIN Pan más frecuente:")
print(sorted_combos_without_pan[0])

print("\nAlgunas combinaciones CON Pan:")
print(sorted_combos_with_pan[:5])

#************* pregunta 4 **************

# calcular frecuencia de todas las duplas
pairs = {}
for combo in combinations(products, 2):
    pairs[combo] = df_numeric.T.loc[list(combo)].all().sum()

# Ordenar de mayor a menor frecuencia
sorted_pairs = sorted(pairs.items(), key=lambda item: item[1], reverse=True)

jamon_queso_freq = pairs.get(('Jamón', 'Queso'))

print(f"Frecuencia de compra conjunta de ('Jamón', 'Queso'): {jamon_queso_freq} veces.")

print("\nPares de productos más frecuentes:")
print(sorted_pairs[:5])

#************* pregunta 5 **************

# ventas totales de Pan
total_pan_sales = df_numeric['Pan'].sum()

# calcular confianza para Pan -> X
confidence_pan_to_x = {}
for product in products:
    if product != 'Pan':
        # compras conjuntas de Pan y el producto X
        joint_sales = df_numeric[(df_numeric['Pan'] == 1) & (df_numeric[product] == 1)].shape[0]
        confidence = (joint_sales / total_pan_sales) * 100
        confidence_pan_to_x[f"Pan -> {product}"] = confidence

# ordenar por confianza
sorted_confidence = sorted(confidence_pan_to_x.items(), key=lambda item: item[1], reverse=True)

print("Confianza de que se compre un producto X, dado que se compró Pan:")
for rule, conf in sorted_confidence:
    print(f"{rule}: {conf:.2f}%")


#************* pregunta 6 **************

# calcular la confianza para todas las reglas X -> Y
all_confidence = {}
for x in products:
    for y in products:
        if x != y:
            # ventas de X
            support_x = df_numeric[x].sum()
            if support_x > 0:
                # ventas conjuntas de X e Y
                support_xy = df_numeric[(df_numeric[x] == 1) & (df_numeric[y] == 1)].shape[0]
                confidence = (support_xy / support_x) * 100
                all_confidence[f"{x} -> {y}"] = confidence

# encontrar el producto con la menor influencia máxima
max_influence = {}
for product in products:
    influences = [v for k, v in all_confidence.items() if k.startswith(product)]
    if influences:
        max_influence[product] = max(influences)

# ordenar por influencia máxima (de menor a mayor)
sorted_max_influence = sorted(max_influence.items(), key=lambda item: item[1])

print("Máxima influencia de cada producto sobre otro (en % de confianza):")
for product, influence in sorted_max_influence:
    print(f"{product}: {influence:.2f}%")

least_influential = sorted_max_influence[0][0]
print(f"\nEl producto con menor influencia es: {least_influential}")

#************* pregunta 7 **************

# datos de la pregunta 6 se ordenan de mayor a menor
strongest_influencers = sorted(max_influence.items(), key=lambda item: item[1], reverse=True)

print("Máxima influencia de cada producto sobre otro (en % de confianza):")
for product, influence in strongest_influencers:
    print(f"{product}: {influence:.2f}%")

most_influential = strongest_influencers[0][0]
print(f"\nEl producto con mayor poder de determinación es: {most_influential}")

# regla específica de mayor confianza
highest_confidence_rule = max(all_confidence, key=all_confidence.get)
print(f"La regla de mayor confianza es '{highest_confidence_rule}' con {all_confidence[highest_confidence_rule]:.2f}%")

#************* pregunta 8 **************

# confianza de Mantequilla -> Queso
butter_sales = df_numeric['Mantequilla'].sum()
butter_cheese_sales = df_numeric[(df_numeric['Mantequilla'] == 1) & (df_numeric['Queso'] == 1)].shape[0]

confidence_butter_to_cheese = (butter_cheese_sales / butter_sales) * 100

print(f"Confianza de la regla 'Mantequilla -> Queso': {confidence_butter_to_cheese:.2f}%")

