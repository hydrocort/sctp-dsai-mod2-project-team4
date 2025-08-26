{{
  config(
    materialized='view'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_sellers') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.seller_id') as seller_id,
        JSON_EXTRACT_SCALAR(data, '$.seller_zip_code_prefix') as seller_zip_code_prefix,
        JSON_EXTRACT_SCALAR(data, '$.seller_city') as seller_city,
        JSON_EXTRACT_SCALAR(data, '$.seller_state') as seller_state,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.seller_id') IS NOT NULL  -- Basic data quality filter
),

cleaned AS (
    SELECT
        -- Primary key
        seller_id,
        
        -- Location data (cleaned and standardized)
        TRIM(seller_zip_code_prefix) as seller_zip_prefix,
        TRIM(seller_city) as seller_city,
        UPPER(TRIM(seller_state)) as seller_state,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
