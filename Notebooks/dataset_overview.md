# Dataset Overview - Initial Data Profiling

## Summary
This document provides an overview of the initial data profiling conducted on our datasets. We analyzed **9 e-commerce datasets** and **2 marketing datasets** to understand their structure, data quality, and characteristics.

## E-Commerce Datasets

### 1. Customers Dataset
- **Shape**: 99,441 rows × 5 columns
- **Memory Usage**: 29.62 MB
- **Columns**: 
  1. `customer_id`
  2. `customer_unique_id`
  3. `customer_zip_code_prefix`
  4. `customer_city`
  5. `customer_state`
- **Data Quality**: ✅ No null values found
- **Data Types**: 4 object columns, 1 integer column

### 2. Orders Dataset
- **Shape**: 99,441 rows × 8 columns
- **Memory Usage**: 58.97 MB
- **Columns**: 
  1. `order_id`
  2. `customer_id`
  3. `order_status`
  4. `order_purchase_timestamp`
  5. `order_approved_at`
  6. `order_delivered_carrier_date`
  7. `order_delivered_customer_date`
  8. `order_estimated_delivery_date`
- **Data Quality**: ⚠️ Contains null values
  - `order_approved_at`: 160 (0.2%)
  - `order_delivered_carrier_date`: 1,783 (1.8%)
  - `order_delivered_customer_date`: 2,965 (3.0%)
- **Data Types**: All 8 columns are object type

### 3. Order Items Dataset
- **Shape**: 112,650 rows × 7 columns
- **Memory Usage**: 39.43 MB
- **Columns**: 
  1. `order_id`
  2. `order_item_id`
  3. `product_id`
  4. `seller_id`
  5. `shipping_limit_date`
  6. `price`
  7. `freight_value`
- **Data Quality**: ✅ No null values found
- **Data Types**: 4 object columns, 2 float columns, 1 integer column

### 4. Order Payments Dataset
- **Shape**: 103,886 rows × 5 columns
- **Memory Usage**: 17.81 MB
- **Columns**: 
  1. `order_id`
  2. `payment_sequential`
  3. `payment_type`
  4. `payment_installments`
  5. `payment_value`
- **Data Quality**: ✅ No null values found
- **Data Types**: 2 object columns, 2 integer columns, 1 float column

### 5. Order Reviews Dataset
- **Shape**: 99,224 rows × 7 columns
- **Memory Usage**: 42.75 MB
- **Columns**: 
  1. `review_id`
  2. `order_id`
  3. `review_score`
  4. `review_comment_title`
  5. `review_comment_message`
  6. `review_creation_date`
  7. `review_answer_timestamp`
- **Data Quality**: ⚠️ Contains significant null values
  - `review_comment_title`: 87,656 (88.3%)
  - `review_comment_message`: 58,247 (58.7%)
- **Data Types**: 6 object columns, 1 integer column

### 6. Products Dataset
- **Shape**: 32,951 rows × 9 columns
- **Memory Usage**: 6.79 MB
- **Columns**: 
  1. `product_id`
  2. `product_category_name`
  3. `product_name_lenght`
  4. `product_description_lenght`
  5. `product_photos_qty`
  6. `product_weight_g`
  7. `product_length_cm`
  8. `product_height_cm`
  9. `product_width_cm`
- **Data Quality**: ⚠️ Contains null values
  - `product_category_name`: 610 (1.9%)
  - `product_name_lenght`: 610 (1.9%)
  - `product_description_lenght`: 610 (1.9%)
  - `product_photos_qty`: 610 (1.9%)
  - `product_weight_g`: 2 (0.0%)
  - `product_length_cm`: 2 (0.0%)
  - `product_height_cm`: 2 (0.0%)
  - `product_width_cm`: 2 (0.0%)
- **Data Types**: 7 float columns, 2 object columns

### 7. Sellers Dataset
- **Shape**: 3,095 rows × 4 columns
- **Memory Usage**: 0.66 MB
- **Columns**: 
  1. `seller_id`
  2. `seller_zip_code_prefix`
  3. `seller_city`
  4. `seller_state`
- **Data Quality**: ✅ No null values found
- **Data Types**: 3 object columns, 1 integer column

### 8. Geolocation Dataset
- **Shape**: 1,000,163 rows × 5 columns
- **Memory Usage**: 145.20 MB
- **Columns**: 
  1. `geolocation_zip_code_prefix`
  2. `geolocation_lat`
  3. `geolocation_lng`
  4. `geolocation_city`
  5. `geolocation_state`
- **Data Quality**: ✅ No null values found
- **Data Types**: 2 float columns, 2 object columns, 1 integer column

### 9. Category Translation Dataset
- **Shape**: 71 rows × 2 columns
- **Memory Usage**: 0.01 MB
- **Columns**: 
  1. `product_category_name`
  2. `product_category_name_english`
- **Data Quality**: ✅ No null values found
- **Data Types**: All 2 columns are object type

## Marketing Datasets

### 1. Marketing Qualified Leads Dataset
- **Shape**: 8,000 rows × 4 columns
- **Memory Usage**: 2.38 MB
- **Columns**: 
  1. `mql_id`
  2. `first_contact_date`
  3. `landing_page_id`
  4. `origin`
- **Data Quality**: ⚠️ Contains minimal null values
  - `origin`: 60 (0.8%)
- **Data Types**: All 4 columns are object type

### 2. Closed Deals Dataset
- **Shape**: 842 rows × 14 columns
- **Memory Usage**: 0.65 MB
- **Columns**: 
  1. `mql_id`
  2. `seller_id`
  3. `sdr_id`
  4. `sr_id`
  5. `won_date`
  6. `business_segment`
  7. `lead_type`
  8. `lead_behaviour_profile`
  9. `has_company`
  10. `has_gtin`
  11. `average_stock`
  12. `business_type`
  13. `declared_product_catalog_size`
  14. `declared_monthly_revenue`
- **Data Quality**: ⚠️ Contains significant null values
  - `business_segment`: 1 (0.1%)
  - `lead_type`: 6 (0.7%)
  - `lead_behaviour_profile`: 177 (21.0%)
  - `has_company`: 779 (92.5%)
  - `has_gtin`: 778 (92.4%)
  - `average_stock`: 776 (92.2%)
  - `business_type`: 10 (1.2%)
  - `declared_product_catalog_size`: 773 (91.8%)
- **Data Types**: 12 object columns, 2 float columns

## Key Observations

### Data Quality Summary
- **Clean Datasets**: 5 out of 11 datasets have no null values
- **Datasets with Missing Data**: 6 datasets contain null values ranging from minimal (0.1%) to significant (92.5%)
- **Total Memory Usage**: ~344 MB across all datasets

### Notable Data Quality Issues
1. **Order Reviews**: High percentage of missing comment titles (88.3%) and messages (58.7%)
2. **Closed Deals**: Very high percentage of missing values in business characteristics (90%+)
3. **Products**: Consistent missing data pattern (610 records missing across multiple fields)

### Dataset Sizes
- **Largest**: Geolocation dataset (1M+ records, 145MB)
- **Smallest**: Category Translation dataset (71 records, 0.01MB)
- **Most Complex**: Closed Deals dataset (14 columns with varied data types)