{{
  config(
    materialized='view'
    schema='staging'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_customers') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.customer_id') as customer_id,
        JSON_EXTRACT_SCALAR(data, '$.customer_unique_id') as customer_unique_id,
        JSON_EXTRACT_SCALAR(data, '$.customer_city') as customer_city,
        JSON_EXTRACT_SCALAR(data, '$.customer_state') as customer_state,
        JSON_EXTRACT_SCALAR(data, '$.customer_zip_code_prefix') as customer_zip_prefix,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.customer_id') IS NOT NULL  -- Basic data quality filter
),

cleaned AS (
    SELECT
        -- Primary key
        customer_id,
        
        -- Customer identifiers
        customer_unique_id,
        
        -- Location data (cleaned and standardized)
        TRIM(customer_city) as customer_city,
        UPPER(TRIM(customer_state)) as customer_state,
        TRIM(customer_zip_prefix) as customer_zip_prefix,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
