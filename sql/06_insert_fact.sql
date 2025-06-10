INSERT INTO netflix_data.content_fact (
    show_id, title, id_type, id_rating, id_genre, id_year,
    director, "cast", date_added, duration, duration_minutes, num_seasons, description
)

SELECT
    ct.show_id,
    ct.title,
    dt.id_type,
    dr.id_rating,
    dg.id_genre,
    dy.id_year,
    ct.director,
    ct."cast",
    ct.date_added,
    ct.original_duration AS duration,
    ct.duration_minutes,
    ct.num_seasons,
    ct.description
FROM netflix_data.clean_titles ct
LEFT JOIN netflix_data.dim_type dt ON TRIM(UPPER(ct.type)) = UPPER(dt.type)
LEFT JOIN netflix_data.dim_rating dr ON TRIM(UPPER(ct.rating)) = UPPER(dr.rating)
LEFT JOIN netflix_data.dim_year dy ON ct.release_year = dy.release_year
LEFT JOIN LATERAL (
    SELECT id_genre
    FROM netflix_data.dim_genre
    WHERE genre = TRIM(split_part(ct.listed_in, ',', 1))
    LIMIT 1
) dg ON true;


