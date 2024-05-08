-- List bands with Glam rock as their main style, ranked by their longevity
SELECT band_name,
       IF(SPLIT(band_lifespan, ' - ')[2] = 'present', 2022 - CAST(SPLIT(band_lifespan, ' - ')[1] AS UNSIGNED), CAST(SPLIT(band_lifespan, ' - ')[2] AS UNSIGNED) - CAST(SPLIT(band_lifespan, ' - ')[1] AS UNSIGNED)) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', main_style)
ORDER BY lifespan DESC, band_name;
