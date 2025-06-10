INSERT INTO netflix_data.content_country_bridge (show_id, id_country)
SELECT DISTINCT
    ct.show_id,
    dc.id_country
FROM netflix_data.clean_titles ct,
     unnest(string_to_array(ct.country, ',')) AS country_name
JOIN netflix_data.dim_country dc ON TRIM(country_name) = dc.country
WHERE ct.country IS NOT NULL;
