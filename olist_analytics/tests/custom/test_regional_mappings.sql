-- Custom test: Regional Mappings Completeness
-- This test validates that all Brazilian states have proper regional classifications
-- and that customer/seller regional assignments are complete

WITH regional_mapping_checks AS (
    -- Test 1: Validate seed data completeness
    -- All 27 Brazilian states + Federal District should be present in brazil_state_regions
    SELECT 
        'seed_data_completeness' as test_name,
        'All 27 Brazilian states + Federal District should be present' as test_description,
        CASE 
            WHEN COUNT(*) = 27 THEN 'PASS'
            ELSE 'FAIL: Expected 27 states, found ' || COUNT(*)::STRING
        END as test_result,
        COUNT(*) as state_count
    FROM {{ ref('brazil_state_regions') }}
    
    UNION ALL
    
    -- Test 2: Validate no duplicate state codes in seed data
    SELECT 
        'seed_data_uniqueness' as test_name,
        'No duplicate state codes should exist' as test_description,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL: Found ' || COUNT(*)::STRING || ' duplicate state codes'
        END as test_result,
        COUNT(*) as duplicate_count
    FROM (
        SELECT state_code, COUNT(*) as cnt
        FROM {{ ref('brazil_state_regions') }}
        GROUP BY state_code
        HAVING COUNT(*) > 1
    ) duplicates
    
    UNION ALL
    
    -- Test 3: Validate all customers have regional assignments
    SELECT 
        'customer_regional_completeness' as test_name,
        'All customers should have regional assignments' as test_description,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL: Found ' || COUNT(*)::STRING || ' customers without regional assignments'
        END as test_result,
        COUNT(*) as unassigned_count
    FROM {{ ref('dim_customers') }}
    WHERE customer_region IS NULL OR customer_economic_zone IS NULL
    
    UNION ALL
    
    -- Test 4: Validate all sellers have regional assignments
    SELECT 
        'seller_regional_completeness' as test_name,
        'All sellers should have regional assignments' as test_description,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL: Found ' || COUNT(*)::STRING || ' sellers without regional assignments'
        END as test_result,
        COUNT(*) as unassigned_count
    FROM {{ ref('dim_sellers') }}
    WHERE seller_region IS NULL OR seller_economic_zone IS NULL
    
    UNION ALL
    
    -- Test 5: Validate regional distribution reasonableness
    -- Check if regional distributions make sense (e.g., Southeast should have more customers/sellers)
    SELECT 
        'regional_distribution_reasonableness' as test_name,
        'Regional distributions should be reasonable (Southeast should be largest)' as test_description,
        CASE 
            WHEN southeast_count > north_count AND southeast_count > northeast_count THEN 'PASS'
            ELSE 'FAIL: Southeast region should have the highest count'
        END as test_result,
        southeast_count as southeast_total
    FROM (
        SELECT 
            SUM(CASE WHEN customer_region = 'Southeast' THEN 1 ELSE 0 END) as southeast_count,
            SUM(CASE WHEN customer_region = 'North' THEN 1 ELSE 0 END) as north_count,
            SUM(CASE WHEN customer_region = 'Northeast' THEN 1 ELSE 0 END) as northeast_count
        FROM {{ ref('dim_customers') }}
    ) regional_counts
    
    UNION ALL
    
    -- Test 6: Validate state code format consistency
    -- All state codes should be exactly 2 characters
    SELECT 
        'state_code_format_consistency' as test_name,
        'All state codes should be exactly 2 characters' as test_description,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL: Found ' || COUNT(*)::STRING || ' invalid state code formats'
        END as test_result,
        COUNT(*) as invalid_format_count
    FROM {{ ref('brazil_state_regions') }}
    WHERE LENGTH(state_code) != 2
    
    UNION ALL
    
    -- Test 7: Validate economic zone assignments
    -- All states should have valid economic zone assignments
    SELECT 
        'economic_zone_assignments' as test_name,
        'All states should have valid economic zone assignments' as test_description,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL: Found ' || COUNT(*)::STRING || ' states without economic zones'
        END as test_result,
        COUNT(*) as missing_economic_zone_count
    FROM {{ ref('brazil_state_regions') }}
    WHERE economic_zone IS NULL OR economic_zone NOT IN ('Amazon', 'Northeast', 'Southeast', 'South', 'Central')
    
    UNION ALL
    
    -- Test 8: Validate regional mapping consistency between customers and sellers
    -- States should have consistent regional assignments across all tables
    SELECT 
        'regional_mapping_consistency' as test_name,
        'Regional assignments should be consistent across all tables' as test_description,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL: Found ' || COUNT(*)::STRING || ' inconsistent regional mappings'
        END as test_result,
        COUNT(*) as inconsistent_count
    FROM (
        SELECT DISTINCT c.customer_state, c.customer_region, s.seller_region
        FROM {{ ref('dim_customers') }} c
        JOIN {{ ref('dim_sellers') }} s ON c.customer_state = s.seller_state
        WHERE c.customer_region != s.seller_region
    ) inconsistencies
)

SELECT 
    test_name,
    test_description,
    test_result,
    CASE 
        WHEN test_result LIKE 'PASS%' THEN 0
        ELSE 1
    END as failed_records
FROM regional_mapping_checks
WHERE test_result LIKE 'FAIL%'

-- This test will fail if any regional mapping issues are found
-- The test passes when all regional mappings are complete and consistent
