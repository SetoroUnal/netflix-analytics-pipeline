import os
import psycopg2
from dotenv import load_dotenv
import subprocess

# Cargar variables de entorno
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 5432))

# Archivos SQL a ejecutar en orden
sql_files = [
    "sql/01_create_schema.sql",
    "sql/02_create_raw_titles.sql",
    "sql/03_transform_clean.sql",
    "sql/04_star_schema.sql",
    "sql/05_insert_dimensions.sql",
    "sql/06_insert_fact.sql",
    "sql/07_insert_country_bridge.sql"
]

def run_load_script():
    print("Ejecutando carga desde KaggleHub...")
    result = subprocess.run(["python", "02.load_raw_from_kagglehub.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error en carga de datos:")
        print(result.stderr)
    else:
        print("Carga completada.")
        print(result.stdout)

def run_all_sql(files):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cur = conn.cursor()
        for filepath in files:
            print(f"Ejecutando: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as file:
                sql = file.read()
                cur.execute(sql)
                conn.commit()
                print(f"Finalizado: {filepath}")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error al ejecutar SQL:", e)

def run_export():
    print("Exportando CSV para dashboard...")
    result = subprocess.run(["python", "03.export_csv.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(" Error al exportar CSV:")
        print(result.stderr)
    else:
        print("Exportación completada.")
        print(result.stdout)

if __name__ == "__main__":
    # Crear esquema
    run_all_sql(["sql/01_create_schema.sql"])
    
    # Crear tabla raw_titles
    run_all_sql(["sql/02_create_raw_titles.sql"])
    
    # Cargar datos a raw_titles
    run_load_script()

    # Ejecutar el resto del pipeline
    run_all_sql(sql_files[2:])
    
    # Validar integridad
    subprocess.run(["python", "04.validate_model.py"], check=True)
    
    # Exportar CSV
    run_export()



