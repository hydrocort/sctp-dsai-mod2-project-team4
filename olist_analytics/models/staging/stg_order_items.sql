{{
  config(
    materialized='view',
    schema='staging'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_order_items') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.order_id') as order_id,
        JSON_EXTRACT_SCALAR(data, '$.order_item_id') as order_item_id,
        JSON_EXTRACT_SCALAR(data, '$.product_id') as product_id,
        JSON_EXTRACT_SCALAR(data, '$.seller_id') as seller_id,
        JSON_EXTRACT_SCALAR(data, '$.shipping_limit_date') as shipping_limit_date,
        JSON_EXTRACT_SCALAR(data, '$.price') as price,
        JSON_EXTRACT_SCALAR(data, '$.freight_value') as freight_value,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.order_id') IS NOT NULL  -- Basic data quality filter
      AND JSON_EXTRACT_SCALAR(data, '$.order_item_id') IS NOT NULL
),

cleaned AS (
    SELECT
        -- Primary keys
        order_id,
        order_item_id,
        
        -- Foreign keys
        product_id,
        seller_id,
        
        -- Shipping information
        CASE 
            WHEN shipping_limit_date != '' THEN TIMESTAMP(shipping_limit_date)
            ELSE NULL 
        END as shipping_limit_date,
        
        -- Numeric values (converted from strings)
        CASE 
            WHEN price != '' AND SAFE_CAST(price AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(price AS FLOAT64)
            ELSE 0.0
        END as price,
        
        CASE 
            WHEN freight_value != '' AND SAFE_CAST(freight_value AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(freight_value AS FLOAT64)
            ELSE 0.0
        END as freight_value,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
