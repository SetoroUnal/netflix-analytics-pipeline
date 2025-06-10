-- Poblar dim_type
INSERT INTO netflix_data.dim_type (type)
SELECT DISTINCT type
FROM netflix_data.clean_titles
WHERE type IS NOT NULL
ON CONFLICT (type) DO NOTHING;

-- Poblar dim_country
INSERT INTO netflix_data.dim_country (country)
SELECT DISTINCT TRIM(unnest(string_to_array(country, ',')))
FROM netflix_data.clean_titles
WHERE country IS NOT NULL
ON CONFLICT (country) DO NOTHING;

-- Poblar dim_rating
INSERT INTO netflix_data.dim_rating (rating)
SELECT DISTINCT rating
FROM netflix_data.clean_titles
WHERE rating IS NOT NULL
ON CONFLICT (rating) DO NOTHING;

-- Poblar dim_genre
INSERT INTO netflix_data.dim_genre (genre)
SELECT DISTINCT TRIM(unnest(string_to_array(listed_in, ',')))
FROM netflix_data.clean_titles
WHERE listed_in IS NOT NULL
ON CONFLICT (genre) DO NOTHING;

-- Poblar dim_year
INSERT INTO netflix_data.dim_year (release_year)
SELECT DISTINCT release_year
FROM netflix_data.clean_titles
WHERE release_year IS NOT NULL
ON CONFLICT (release_year) DO NOTHING;

