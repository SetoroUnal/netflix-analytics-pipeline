DROP TABLE IF EXISTS netflix_data.clean_titles;

CREATE TABLE netflix_data.clean_titles AS
SELECT
    show_id,
    type,
    title,
    -- Reemplazamos valores vacíos por 'Unknown' y quitamos espacios
    COALESCE(NULLIF(TRIM(director), ''), 'Unknown') AS director,
    COALESCE(NULLIF(TRIM("cast"), ''), 'Unknown') AS "cast",
    COALESCE(NULLIF(TRIM(country), ''), 'Unknown') AS country,
    
    -- Convertimos date_added a tipo DATE si no lo es
    date_added,
    
    release_year,
    rating,
    TRIM(duration) AS original_duration,
    
    -- Extraemos duración en minutos para películas
    CASE
        WHEN type = 'Movie' AND duration LIKE '%min%' THEN
            CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER)
        ELSE NULL
    END AS duration_minutes,
    
    -- Extraemos cantidad de temporadas para series
    CASE
        WHEN type = 'TV Show' AND duration LIKE '%Season%' THEN
            CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER)
        ELSE NULL
    END AS num_seasons,
    
    listed_in,
    description
FROM
    netflix_data.raw_titles;
