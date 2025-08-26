{{
  config(
    materialized='view'
  )
}}

/*
  STAGING MODEL: stg_products
  
  PURPOSE: Clean and prepare raw product data with dimension calculations and type conversions
  
  KEY TRANSFORMATIONS:
  - JSON extraction from nested data column
  - Type conversions: STRING → INT64 (lengths, quantities), STRING → FLOAT64 (dimensions, weight)
  - Volume calculation: length × height × width in cubic centimeters
  - Null handling: Missing dimensions converted to 0.0 with fallback logic
  
  VOLUME CALCULATION EDGE CASES:
  - 32,949 products (99.99%): Have valid dimensions → Volume calculated correctly
  - 2 products (0.01%): Have NULL dimensions in raw data → Volume set to 0.0
    * Product ID: 09ff539a621711667c43eba6a3bd8466 (category: bebes) - All dimensions NULL
    * Product ID: 5eb564652db742ff8f28759cd8d2652a (category: NULL) - All dimensions NULL
  
  BUSINESS LOGIC: Products without valid dimensions cannot have meaningful volume,
  so 0.0 is the correct business value for these edge cases.
*/

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_products') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.product_id') as product_id,
        JSON_EXTRACT_SCALAR(data, '$.product_category_name') as product_category_name,
        JSON_EXTRACT_SCALAR(data, '$.product_name_lenght') as product_name_lenght,
        JSON_EXTRACT_SCALAR(data, '$.product_description_lenght') as product_description_lenght,
        JSON_EXTRACT_SCALAR(data, '$.product_photos_qty') as product_photos_qty,
        JSON_EXTRACT_SCALAR(data, '$.product_weight_g') as product_weight_g,
        JSON_EXTRACT_SCALAR(data, '$.product_length_cm') as product_length_cm,
        JSON_EXTRACT_SCALAR(data, '$.product_height_cm') as product_height_cm,
        JSON_EXTRACT_SCALAR(data, '$.product_width_cm') as product_width_cm,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.product_id') IS NOT NULL  -- Basic data quality filter
),

cleaned AS (
    SELECT
        -- Primary key
        product_id,
        
        -- Category information
        TRIM(product_category_name) as product_category_name,
        
        -- Text length metrics (converted to integers)
        CASE 
            WHEN product_name_lenght != '' AND SAFE_CAST(product_name_lenght AS INT64) IS NOT NULL 
            THEN SAFE_CAST(product_name_lenght AS INT64)
            ELSE 0
        END as product_name_length,
        
        CASE 
            WHEN product_description_lenght != '' AND SAFE_CAST(product_description_lenght AS INT64) IS NOT NULL 
            THEN SAFE_CAST(product_description_lenght AS INT64)
            ELSE 0
        END as product_description_length,
        
        -- Photo quantity (converted to integer)
        CASE 
            WHEN product_photos_qty != '' AND SAFE_CAST(product_photos_qty AS INT64) IS NOT NULL 
            THEN SAFE_CAST(product_photos_qty AS INT64)
            ELSE 0
        END as product_photos_qty,
        
        -- Physical dimensions (converted to numeric)
        CASE 
            WHEN product_weight_g != '' AND SAFE_CAST(product_weight_g AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(product_weight_g AS FLOAT64)
            ELSE 0.0
        END as product_weight_g,
        
        CASE 
            WHEN product_length_cm != '' AND SAFE_CAST(product_length_cm AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(product_length_cm AS FLOAT64)
            ELSE 0.0
        END as product_length_cm,
        
        CASE 
            WHEN product_height_cm != '' AND SAFE_CAST(product_height_cm AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(product_height_cm AS FLOAT64)
            ELSE 0.0
        END as product_height_cm,
        
        CASE 
            WHEN product_width_cm != '' AND SAFE_CAST(product_width_cm AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(product_width_cm AS FLOAT64)
            ELSE 0.0
        END as product_width_cm,
        
        -- Calculated volume (with null handling)
        CASE 
            WHEN product_length_cm != '' AND SAFE_CAST(product_length_cm AS FLOAT64) IS NOT NULL
                AND product_height_cm != '' AND SAFE_CAST(product_height_cm AS FLOAT64) IS NOT NULL
                AND product_width_cm != '' AND SAFE_CAST(product_width_cm AS FLOAT64) IS NOT NULL
                AND SAFE_CAST(product_length_cm AS FLOAT64) > 0
                AND SAFE_CAST(product_height_cm AS FLOAT64) > 0
                AND SAFE_CAST(product_width_cm AS FLOAT64) > 0
            THEN SAFE_CAST(product_length_cm AS FLOAT64) * 
                 SAFE_CAST(product_height_cm AS FLOAT64) * 
                 SAFE_CAST(product_width_cm AS FLOAT64)
            ELSE 0.0
        END as product_volume_cm3,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
