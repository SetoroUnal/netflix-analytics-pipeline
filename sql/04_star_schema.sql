-- Eliminar las tablas si ya existen
DROP TABLE IF EXISTS netflix_data.content_fact CASCADE;
DROP TABLE IF EXISTS netflix_data.dim_type CASCADE;
DROP TABLE IF EXISTS netflix_data.dim_country CASCADE;
DROP TABLE IF EXISTS netflix_data.dim_rating CASCADE;
DROP TABLE IF EXISTS netflix_data.dim_genre CASCADE;
DROP TABLE IF EXISTS netflix_data.dim_year CASCADE;

-- Crear dimensiones
CREATE TABLE netflix_data.dim_type (
    id_type SERIAL PRIMARY KEY,
    type TEXT UNIQUE NOT NULL
);

CREATE TABLE netflix_data.dim_country (
    id_country SERIAL PRIMARY KEY,
    country TEXT UNIQUE NOT NULL
);

CREATE TABLE netflix_data.dim_rating (
    id_rating SERIAL PRIMARY KEY,
    rating TEXT UNIQUE NOT NULL
);

CREATE TABLE netflix_data.dim_genre (
    id_genre SERIAL PRIMARY KEY,
    genre TEXT UNIQUE NOT NULL
);

CREATE TABLE netflix_data.dim_year (
    id_year SERIAL PRIMARY KEY,
    release_year INTEGER UNIQUE NOT NULL
);

-- Crear tabla de hechos
CREATE TABLE netflix_data.content_fact (
    show_id TEXT PRIMARY KEY,
    title TEXT,
    id_type INTEGER REFERENCES netflix_data.dim_type(id_type),
    id_country INTEGER REFERENCES netflix_data.dim_country(id_country),
    id_rating INTEGER REFERENCES netflix_data.dim_rating(id_rating),
    id_genre INTEGER REFERENCES netflix_data.dim_genre(id_genre),
    id_year INTEGER REFERENCES netflix_data.dim_year(id_year),
    director TEXT,
    "cast" TEXT,
    date_added DATE,
    duration TEXT,
    duration_minutes INTEGER,
    num_seasons INTEGER,
    description TEXT
);
-- TABLA PUENTE 
DROP TABLE IF EXISTS netflix_data.content_country_bridge CASCADE;

ALTER TABLE netflix_data.content_fact DROP CONSTRAINT IF EXISTS content_fact_id_country_fkey;
ALTER TABLE netflix_data.content_fact DROP COLUMN IF EXISTS id_country;

CREATE TABLE netflix_data.content_country_bridge (
    show_id TEXT REFERENCES netflix_data.content_fact(show_id),
    id_country INTEGER REFERENCES netflix_data.dim_country(id_country),
    PRIMARY KEY (show_id, id_country)
);
