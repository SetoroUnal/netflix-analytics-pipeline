import pandas as pd
import os

# Ruta relativa al archivo dentro del proyecto
input_path = os.path.join(os.getcwd(), "netflix_dash_ready.csv")
output_path = os.path.join(os.getcwd(), "netflix_global_unique.csv")

# Leer el CSV original
df = pd.read_csv(input_path)

# Ordenar para que se prioricen países válidos sobre "Unknown"
df_sorted = df.sort_values(by=["show_id", "country"], ascending=[True, True])

# Eliminar duplicados por show_id, manteniendo el primer país válido
df_unique = df_sorted.drop_duplicates(subset="show_id", keep="first")

# Exportar nuevo archivo
df_unique.to_csv(output_path, index=False)

print("Archivo 'netflix_global_unique.csv' generado correctamente.")
