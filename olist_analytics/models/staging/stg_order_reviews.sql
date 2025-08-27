{{
  config(
    materialized='view',
    schema='staging'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('olist_raw', 'main_raw_order_reviews') }}
),

extracted AS (
    SELECT
        -- Extract data from JSON column
        JSON_EXTRACT_SCALAR(data, '$.review_id') as review_id,
        JSON_EXTRACT_SCALAR(data, '$.order_id') as order_id,
        JSON_EXTRACT_SCALAR(data, '$.review_score') as review_score,
        JSON_EXTRACT_SCALAR(data, '$.review_comment_title') as review_comment_title,
        JSON_EXTRACT_SCALAR(data, '$.review_comment_message') as review_comment_message,
        JSON_EXTRACT_SCALAR(data, '$.review_creation_date') as review_creation_date,
        JSON_EXTRACT_SCALAR(data, '$.review_answer_timestamp') as review_answer_timestamp,
        
        -- Metadata columns
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM source
    WHERE JSON_EXTRACT_SCALAR(data, '$.review_id') IS NOT NULL  -- Basic data quality filter
      AND JSON_EXTRACT_SCALAR(data, '$.order_id') IS NOT NULL
),

cleaned AS (
    SELECT
        -- Primary key
        review_id,
        
        -- Foreign key
        order_id,
        
        -- Review score (validated and converted to integer)
        CASE 
            WHEN review_score != '' AND SAFE_CAST(review_score AS INT64) IS NOT NULL 
            THEN SAFE_CAST(review_score AS INT64)
            ELSE NULL
        END as review_score,
        
        -- Comment availability flags
        CASE 
            WHEN review_comment_title IS NOT NULL AND review_comment_title != '' THEN TRUE
            ELSE FALSE
        END as has_comment_title,
        
        CASE 
            WHEN review_comment_message IS NOT NULL AND review_comment_message != '' THEN TRUE
            ELSE FALSE
        END as has_comment_message,
        
        -- Comment text (cleaned)
        TRIM(review_comment_title) as review_comment_title,
        TRIM(review_comment_message) as review_comment_message,
        
        -- Timestamps (parsed and validated)
        CASE 
            WHEN review_creation_date != '' THEN TIMESTAMP(review_creation_date)
            ELSE NULL 
        END as review_creation_date,
        
        CASE 
            WHEN review_answer_timestamp != '' THEN TIMESTAMP(review_answer_timestamp)
            ELSE NULL 
        END as review_answer_timestamp,
        
        -- Metadata
        _sdc_extracted_at,
        _sdc_table_version
        
    FROM extracted
)

SELECT * FROM cleaned
