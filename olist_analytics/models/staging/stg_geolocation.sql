{{
  config(
    materialized='view'
    schema='staging'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_geolocation') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.geolocation_zip_code_prefix') as geolocation_zip_code_prefix,
        JSON_EXTRACT_SCALAR(data, '$.geolocation_lat') as geolocation_lat,
        JSON_EXTRACT_SCALAR(data, '$.geolocation_lng') as geolocation_lng,
        JSON_EXTRACT_SCALAR(data, '$.geolocation_city') as geolocation_city,
        JSON_EXTRACT_SCALAR(data, '$.geolocation_state') as geolocation_state,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.geolocation_zip_code_prefix') IS NOT NULL  -- Basic data quality filter
),

converted AS (
    SELECT
        -- Zip code prefix
        TRIM(geolocation_zip_code_prefix) as geolocation_zip_code_prefix,
        
        -- Coordinates (converted to numeric)
        CASE 
            WHEN geolocation_lat != '' AND SAFE_CAST(geolocation_lat AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(geolocation_lat AS FLOAT64)
            ELSE NULL
        END as geolocation_lat,
        
        CASE 
            WHEN geolocation_lng != '' AND SAFE_CAST(geolocation_lng AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(geolocation_lng AS FLOAT64)
            ELSE NULL
        END as geolocation_lng,
        
        -- Location information (cleaned)
        TRIM(geolocation_city) as geolocation_city,
        UPPER(TRIM(geolocation_state)) as geolocation_state,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
),

cleaned AS (
    SELECT
        geolocation_zip_code_prefix,
        geolocation_lat,
        geolocation_lng,
        geolocation_city,
        geolocation_state,
        
        -- Coordinate validation flags (now with proper types)
        CASE 
            WHEN geolocation_lat IS NOT NULL 
                AND geolocation_lat >= -90.0 
                AND geolocation_lat <= 90.0      -- Valid latitude range
                AND geolocation_lng IS NOT NULL 
                AND geolocation_lng >= -180.0 
                AND geolocation_lng <= 180.0     -- Valid longitude range
            THEN TRUE
            ELSE FALSE
        END as has_valid_coordinates,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM converted
)

SELECT * FROM cleaned
