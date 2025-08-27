{{
  config(
    materialized='table',
    schema='olist_marts'
  )
}}

WITH review_base AS (
  SELECT
    -- Primary key
    order_id as review_key,
    
    -- Review attributes (already cleaned in staging)
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date
    
  FROM {{ ref('stg_order_reviews') }}
  WHERE order_id IS NOT NULL
),

review_metrics AS (
  SELECT
    r.*,
    
    -- Comment availability flags (TRUE if comment exists, FALSE if empty/null)
    CASE 
      WHEN review_comment_title IS NOT NULL AND review_comment_title != '' THEN TRUE
      ELSE FALSE
    END as has_comment_title,
    
    CASE 
      WHEN review_comment_message IS NOT NULL AND review_comment_message != '' THEN TRUE
      ELSE FALSE
    END as has_comment_message,
    
    -- Review timing: days from order purchase to review creation
    CASE 
      WHEN review_creation_date IS NOT NULL 
        AND EXISTS (
          SELECT 1 FROM {{ ref('stg_orders') }} o 
          WHERE o.order_id = r.review_key 
          AND o.order_purchase_timestamp IS NOT NULL
        )
      THEN (
        SELECT DATE_DIFF(
          DATE(r.review_creation_date), 
          DATE(o.order_purchase_timestamp), 
          DAY
        )
        FROM {{ ref('stg_orders') }} o 
        WHERE o.order_id = r.review_key
      )
      ELSE NULL
    END as days_to_review
    
  FROM review_base r
)

SELECT * FROM review_metrics
ORDER BY review_key
