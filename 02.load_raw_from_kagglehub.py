import os
import pandas as pd
import kagglehub
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Descargar dataset desde KaggleHub
path = kagglehub.dataset_download("rahulvyasm/netflix-movies-and-tv-shows")
csv_file = os.path.join(path, "netflix_titles.csv")

# Leer CSV con limpieza básica
df = pd.read_csv(csv_file, encoding="latin1")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.rename(columns={"cast": "cast_names"}, inplace=True)
df.fillna(value=pd.NA, inplace=True)

# Conectar a PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
cur = conn.cursor()

# Borrar y recrear la tabla temporalmente (opcional)
cur.execute("TRUNCATE netflix_data.raw_titles;")
conn.commit()

# Insertar los datos manualmente
insert_query = '''
INSERT INTO netflix_data.raw_titles (
    show_id, type, title, director, "cast" , country,
    date_added, release_year, rating, duration, listed_in, description
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

data = df.where(pd.notnull(df), None).values.tolist()
cur.executemany(insert_query, data)
conn.commit()

cur.close()
conn.close()

print("Datos cargados exitosamente usando psycopg2.")
