import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 5432))

def log_issue(issue):
    with open("validation_log.txt", "a", encoding="utf-8") as f:
        f.write(issue + "\n")

def run_validation():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cur = conn.cursor()

        validations = {
            "Tabla de hechos poblada":
                "SELECT COUNT(*) FROM netflix_data.content_fact",
            "Dimensiones válidas (type)": 
                """SELECT COUNT(*) FROM netflix_data.content_fact cf
                   LEFT JOIN netflix_data.dim_type dt ON cf.id_type = dt.id_type
                   WHERE dt.id_type IS NULL""",
            "Dimensiones válidas (rating)": 
                """SELECT COUNT(*) FROM netflix_data.content_fact cf
                   LEFT JOIN netflix_data.dim_rating dr ON cf.id_rating = dr.id_rating
                   WHERE dr.id_rating IS NULL""",
            "Dimensiones válidas (year)": 
                """SELECT COUNT(*) FROM netflix_data.content_fact cf
                   LEFT JOIN netflix_data.dim_year dy ON cf.id_year = dy.id_year
                   WHERE dy.id_year IS NULL""",
            "Dimensiones válidas (genre)": 
                """SELECT COUNT(*) FROM netflix_data.content_fact cf
                   LEFT JOIN netflix_data.dim_genre dg ON cf.id_genre = dg.id_genre
                   WHERE dg.id_genre IS NULL""",
            "Nulos en claves críticas":
                """SELECT COUNT(*) FROM netflix_data.content_fact
                   WHERE show_id IS NULL OR title IS NULL OR id_type IS NULL""",
            "Duplicados en show_id":
                """SELECT COUNT(*) FROM (
                   SELECT show_id FROM netflix_data.content_fact
                   GROUP BY show_id HAVING COUNT(*) > 1
                   ) t""",
            "Tabla puente poblada":
                "SELECT COUNT(*) FROM netflix_data.content_country_bridge"
        }

        print("Resultado de validaciones:")

        for label, query in validations.items():
            cur.execute(query)
            result = cur.fetchone()[0]
            if result == 0 and "poblada" in label:
                msg = f"{label} está vacía."
                print(f" - {msg}")
                log_issue(msg)
            elif result > 0 and "válidas" in label:
                msg = f"{label}: {result} registros con FK inválidas."
                print(f" - {msg}")
                log_issue(msg)
            elif result > 0 and "Nulos" in label:
                msg = f"{label}: {result} nulos encontrados."
                print(f" - {msg}")
                log_issue(msg)
            elif result > 0 and "Duplicados" in label:
                msg = f"{label}: {result} duplicados encontrados."
                print(f" - {msg}")
                log_issue(msg)
            else:
                print(f" - {label}: OK")

        cur.close()
        conn.close()
        print("Validación completada (errores posibles logueados en validation_log.txt)")

    except Exception as ex:
        print("Error inesperado:", ex)

if __name__ == "__main__":
    run_validation()
