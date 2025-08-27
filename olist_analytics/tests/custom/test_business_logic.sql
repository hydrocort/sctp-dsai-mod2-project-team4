-- Custom test: Business Logic Validation
-- This test validates critical business calculations and logic rules

WITH business_logic_checks AS (
    -- Test 1: Validate total_item_value calculation (price + freight_value)
    SELECT 
        'total_item_value_calculation' as test_name,
        'total_item_value should equal item_price + freight_value' as test_description,
        COUNT(*) as failed_records
    FROM {{ ref('fact_sales') }}
    WHERE ABS(total_item_value - (item_price + freight_value)) > 0.01  -- Allow for small rounding differences
    
    UNION ALL
    
    -- Test 2: Validate that payment_value is reasonable compared to total_item_value
    -- Payment value should be close to total item value (allowing for multi-item orders and promotions)
    SELECT 
        'payment_value_reasonableness' as test_name,
        'Payment value should be reasonable compared to item value' as test_description,
        COUNT(*) as failed_records
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_orders') }} o ON f.order_key = o.order_key
    WHERE f.payment_value < f.total_item_value * 0.1  -- Payment should not be less than 10% of item value (allows promotions)
       OR f.payment_value > f.total_item_value * 20   -- Payment should not be more than 20x item value (allows high-value orders)
    
    UNION ALL
    
    -- Test 3: Validate delivery performance logic
    -- If delivered, days_to_delivery should be positive
    SELECT 
        'delivery_performance_logic' as test_name,
        'Delivered orders should have positive days_to_delivery' as test_description,
        COUNT(*) as failed_records
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_orders') }} o ON f.order_key = o.order_key
    WHERE o.order_status = 'delivered' 
      AND o.days_to_delivery <= 0
    
    UNION ALL
    
    -- Test 4: Validate on-time delivery flag logic
    -- is_delivered_on_time should be TRUE when delivery_vs_estimate_days <= 0
    SELECT 
        'on_time_delivery_flag_logic' as test_name,
        'On-time delivery flag should match actual vs estimated days' as test_description,
        COUNT(*) as failed_records
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_orders') }} o ON f.order_key = o.order_key
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
      AND (
          (o.delivery_vs_estimate_days <= 0 AND o.is_delivered_on_time = FALSE) OR
          (o.delivery_vs_estimate_days > 0 AND o.is_delivered_on_time = TRUE)
      )
    
    UNION ALL
    
    -- Test 5: Validate review timing logic
    -- days_to_review should be reasonable (allowing for same-day reviews, flagging only clearly wrong dates)
    SELECT 
        'review_timing_logic' as test_name,
        'Review timing should be reasonable (not more than 1 day before order)' as test_description,
        COUNT(*) as failed_records
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_reviews') }} r ON f.review_key = r.review_key
    WHERE r.days_to_review < -1  -- Allow same-day reviews (0 days), flag only clearly wrong dates
    
    UNION ALL
    
    -- Test 6: Validate payment aggregation logic
    -- Payment method flags should be consistent with actual payment data
    SELECT 
        'payment_aggregation_logic' as test_name,
        'Payment method flags should be consistent' as test_description,
        COUNT(*) as failed_records
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_payments') }} p ON f.payment_key = p.payment_key
    WHERE (p.uses_credit_card = TRUE AND p.primary_payment_type != 'credit_card') OR
          (p.uses_boleto = TRUE AND p.primary_payment_type != 'boleto') OR
          (p.uses_voucher = TRUE AND p.primary_payment_type != 'voucher')
    
    UNION ALL
    
    -- Test 7: Validate product volume calculation
    -- Product volume should equal length * height * width when all dimensions are available
    SELECT 
        'product_volume_calculation' as test_name,
        'Product volume should match calculated dimensions' as test_description,
        COUNT(*) as failed_records
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_products') }} p ON f.product_key = p.product_key
    WHERE p.product_length_cm IS NOT NULL 
      AND p.product_height_cm IS NOT NULL 
      AND p.product_width_cm IS NOT NULL
      AND ABS(p.product_volume_cm3 - (p.product_length_cm * p.product_height_cm * p.product_width_cm)) > 0.01
)

SELECT 
    test_name,
    test_description,
    failed_records
FROM business_logic_checks
WHERE failed_records > 0

-- This test will fail if any business logic violations are found
-- The test passes when all business rules are satisfied
