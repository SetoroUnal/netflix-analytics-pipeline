import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

# Conexión a la base de datos
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

# Consulta para tabla desnormalizada
query = """
SELECT
    cf.show_id,
    cf.title,
    dt.type,
    COALESCE(dc.country, 'Unknown') AS country,
    dr.rating,
    dg.genre,
    dy.release_year,
    cf.director,
    cf."cast",
    cf.date_added,
    cf.duration,
    cf.duration_minutes,
    cf.num_seasons,
    cf.description
FROM netflix_data.content_fact cf
LEFT JOIN netflix_data.content_country_bridge ccb ON cf.show_id = ccb.show_id
LEFT JOIN netflix_data.dim_country dc ON ccb.id_country = dc.id_country
LEFT JOIN netflix_data.dim_type dt ON cf.id_type = dt.id_type
LEFT JOIN netflix_data.dim_rating dr ON cf.id_rating = dr.id_rating
LEFT JOIN netflix_data.dim_genre dg ON cf.id_genre = dg.id_genre
LEFT JOIN netflix_data.dim_year dy ON cf.id_year = dy.id_year;
"""


# Ejecutar y exportar
df = pd.read_sql_query(query, conn)
df.to_csv("netflix_dash_ready.csv", index=False)
print(" Archivo 'netflix_dash_ready.csv' exportado exitosamente.")

conn.close()