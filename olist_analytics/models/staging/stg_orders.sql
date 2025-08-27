{{
  config(
    materialized='view',
    schema='staging'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_orders') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.order_id') as order_id,
        JSON_EXTRACT_SCALAR(data, '$.customer_id') as customer_id,
        JSON_EXTRACT_SCALAR(data, '$.order_status') as order_status,
        JSON_EXTRACT_SCALAR(data, '$.order_purchase_timestamp') as order_purchase_timestamp,
        JSON_EXTRACT_SCALAR(data, '$.order_approved_at') as order_approved_at,
        JSON_EXTRACT_SCALAR(data, '$.order_delivered_carrier_date') as order_delivered_carrier_date,
        JSON_EXTRACT_SCALAR(data, '$.order_delivered_customer_date') as order_delivered_customer_date,
        JSON_EXTRACT_SCALAR(data, '$.order_estimated_delivery_date') as order_estimated_delivery_date,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.order_id') IS NOT NULL  -- Basic data quality filter
),

cleaned AS (
    SELECT
        -- Primary key
        order_id,
        
        -- Foreign key
        customer_id,
        
        -- Order status (standardized)
        UPPER(TRIM(order_status)) as order_status,
        
        -- Timestamps (using BigQuery's flexible TIMESTAMP function)
        CASE 
            WHEN order_purchase_timestamp != '' THEN TIMESTAMP(order_purchase_timestamp)
            ELSE NULL 
        END as order_purchase_timestamp,
        
        CASE 
            WHEN order_approved_at != '' THEN TIMESTAMP(order_approved_at)
            ELSE NULL 
        END as order_approved_at,
        
        CASE 
            WHEN order_delivered_carrier_date != '' THEN TIMESTAMP(order_delivered_carrier_date)
            ELSE NULL 
        END as order_delivered_carrier_date,
        
        CASE 
            WHEN order_delivered_customer_date != '' THEN TIMESTAMP(order_delivered_customer_date)
            ELSE NULL 
        END as order_delivered_customer_date,
        
        CASE 
            WHEN order_estimated_delivery_date != '' THEN TIMESTAMP(order_estimated_delivery_date)
            ELSE NULL 
        END as order_estimated_delivery_date,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
