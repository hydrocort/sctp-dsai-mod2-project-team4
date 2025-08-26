{{
  config(
    materialized='view'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_category_translation') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.product_category_name') as product_category_name,
        JSON_EXTRACT_SCALAR(data, '$.product_category_name_english') as product_category_name_english,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.product_category_name') IS NOT NULL  -- Basic data quality filter
      AND JSON_EXTRACT_SCALAR(data, '$.product_category_name_english') IS NOT NULL
),

cleaned AS (
    SELECT
        -- Category names (cleaned and normalized)
        TRIM(product_category_name) as product_category_name,
        TRIM(product_category_name_english) as product_category_name_english,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
