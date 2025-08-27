{{
  config(
    materialized='view',
    schema='staging'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_order_payments') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.order_id') as order_id,
        JSON_EXTRACT_SCALAR(data, '$.payment_sequential') as payment_sequential,
        JSON_EXTRACT_SCALAR(data, '$.payment_type') as payment_type,
        JSON_EXTRACT_SCALAR(data, '$.payment_installments') as payment_installments,
        JSON_EXTRACT_SCALAR(data, '$.payment_value') as payment_value,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.order_id') IS NOT NULL  -- Basic data quality filter
),

cleaned AS (
    SELECT
        -- Foreign key
        order_id,
        
        -- Payment sequence
        CASE 
            WHEN payment_sequential != '' AND SAFE_CAST(payment_sequential AS INT64) IS NOT NULL 
            THEN SAFE_CAST(payment_sequential AS INT64)
            ELSE 1
        END as payment_sequential,
        
        -- Payment type (standardized)
        UPPER(TRIM(payment_type)) as payment_type,
        
        -- Installments (converted to integer)
        CASE 
            WHEN payment_installments != '' AND SAFE_CAST(payment_installments AS INT64) IS NOT NULL 
            THEN SAFE_CAST(payment_installments AS INT64)
            ELSE 1
        END as payment_installments,
        
        -- Payment value (converted to numeric)
        CASE 
            WHEN payment_value != '' AND SAFE_CAST(payment_value AS FLOAT64) IS NOT NULL 
            THEN SAFE_CAST(payment_value AS FLOAT64)
            ELSE 0.0
        END as payment_value,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
