-- Custom test: Referential Integrity between Fact and Dimensions
-- This test ensures that all NON-NULL foreign keys in fact_sales reference valid primary keys in dimension tables
-- NULL foreign keys are allowed and will not cause referential integrity failures

WITH fact_dimension_checks AS (
    -- Check order_key references in fact_sales vs dim_orders
    SELECT 
        'order_key' as foreign_key_column,
        'dim_orders' as dimension_table,
        COUNT(*) as orphaned_records
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_orders') }} d ON f.order_key = d.order_key
    WHERE f.order_key IS NOT NULL AND d.order_key IS NULL
    
    UNION ALL
    
    -- Check customer_key references in fact_sales vs dim_customers
    SELECT 
        'customer_key' as foreign_key_column,
        'dim_customers' as dimension_table,
        COUNT(*) as orphaned_records
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_customers') }} d ON f.customer_key = d.customer_key
    WHERE f.customer_key IS NOT NULL AND d.customer_key IS NULL
    
    UNION ALL
    
    -- Check product_key references in fact_sales vs dim_products
    SELECT 
        'product_key' as foreign_key_column,
        'dim_products' as dimension_table,
        COUNT(*) as orphaned_records
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_products') }} d ON f.product_key = d.product_key
    WHERE f.product_key IS NOT NULL AND d.product_key IS NULL
    
    UNION ALL
    
    -- Check seller_key references in fact_sales vs dim_sellers
    SELECT 
        'seller_key' as foreign_key_column,
        'dim_sellers' as dimension_table,
        COUNT(*) as orphaned_records
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_sellers') }} d ON f.seller_key = d.seller_key
    WHERE f.seller_key IS NOT NULL AND d.seller_key IS NULL
    
    UNION ALL
    
    -- Check date_key references in fact_sales vs dim_date
    SELECT 
        'date_key' as foreign_key_column,
        'dim_date' as dimension_table,
        COUNT(*) as orphaned_records
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_date') }} d ON f.date_key = d.date_key
    WHERE f.date_key IS NOT NULL AND d.date_key IS NULL
    
    UNION ALL
    
    -- Check payment_key references in fact_sales vs dim_payments
    SELECT 
        'payment_key' as foreign_key_column,
        'dim_payments' as dimension_table,
        COUNT(*) as orphaned_records
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_payments') }} d ON f.payment_key = d.payment_key
    WHERE f.payment_key IS NOT NULL AND d.payment_key IS NULL
    
    UNION ALL
    
    -- Check review_key references in fact_sales vs dim_reviews (nullable, so only check non-null values)
    SELECT 
        'review_key' as foreign_key_column,
        'dim_reviews' as dimension_table,
        COUNT(*) as orphaned_records
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_reviews') }} d ON f.review_key = d.review_key
    WHERE f.review_key IS NOT NULL AND d.review_key IS NULL
)

SELECT 
    foreign_key_column,
    dimension_table,
    orphaned_records
FROM fact_dimension_checks
WHERE orphaned_records > 0

-- This test will fail if any orphaned records are found
-- The test passes when all foreign keys reference valid primary keys
