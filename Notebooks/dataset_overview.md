# Dataset Overview - Initial Data Profiling

## Summary
This document provides an overview of the initial data profiling conducted on our datasets. We analyzed **9 e-commerce datasets** and **2 marketing datasets** to understand their structure, data quality, and characteristics.

## E-Commerce Datasets

### 1. Customers Dataset
- **Shape**: 99,441 rows × 5 columns
- **Memory Usage**: 29.62 MB
- **Columns**: 
  1. `customer_id` - Unique identifier for each customer
  2. `customer_unique_id` - Unique identifier for each customer across multiple orders
  3. `customer_zip_code_prefix` - First five digits of the customer's zip code
  4. `customer_city` - City where the customer is located
  5. `customer_state` - State where the customer is located
- **Data Quality**: ✅ No null values found
- **Data Types**: 4 object columns, 1 integer column

### 2. Orders Dataset
- **Shape**: 99,441 rows × 8 columns
- **Memory Usage**: 58.97 MB
- **Columns**: 
  1. `order_id` - Unique identifier for each order
  2. `customer_id` - Identifier linking the order to a customer
  3. `order_status` - Current status of the order (e.g., delivered, shipped, canceled)
  4. `order_purchase_timestamp` - Timestamp when the order was placed
  5. `order_approved_at` - Timestamp when the order payment was approved
  6. `order_delivered_carrier_date` - Date when the order was handed over to the logistic partner
  7. `order_delivered_customer_date` - Date when the order was delivered to the customer
  8. `order_estimated_delivery_date` - Estimated delivery date provided to the customer
- **Data Quality**: ⚠️ Contains null values
  - `order_approved_at`: 160 (0.2%)
  - `order_delivered_carrier_date`: 1,783 (1.8%)
  - `order_delivered_customer_date`: 2,965 (3.0%)
- **Data Types**: All 8 columns are object type

### 3. Order Items Dataset
- **Shape**: 112,650 rows × 7 columns
- **Memory Usage**: 39.43 MB
- **Columns**: 
  1. `order_id` - Identifier linking the item to an order
  2. `order_item_id` - Sequential number identifying the item within the order
  3. `product_id` - Identifier for the product being purchased
  4. `seller_id` - Identifier for the seller of the product
  5. `shipping_limit_date` - Deadline for the seller to ship the product
  6. `price` - Item price paid by the customer
  7. `freight_value` - Shipping cost charged to the customer for this item
- **Data Quality**: ✅ No null values found
- **Data Types**: 4 object columns, 2 float columns, 1 integer column

### 4. Order Payments Dataset
- **Shape**: 103,886 rows × 5 columns
- **Memory Usage**: 17.81 MB
- **Columns**: 
  1. `order_id` - Identifier linking the payment to an order
  2. `payment_sequential` - Sequential number of the payment within the order
  3. `payment_type` - Method of payment used (e.g., credit card, boleto, voucher)
  4. `payment_installments` - Number of installments chosen by the customer
  5. `payment_value` - Transaction value paid by the customer
- **Data Quality**: ✅ No null values found
- **Data Types**: 2 object columns, 2 integer columns, 1 float column

### 5. Order Reviews Dataset
- **Shape**: 99,224 rows × 7 columns
- **Memory Usage**: 42.75 MB
- **Columns**: 
  1. `review_id` - Unique identifier for each review
  2. `order_id` - Identifier linking the review to an order
  3. `review_score` - Rating given by the customer (1 to 5 stars)
  4. `review_comment_title` - Title of the review comment written by the customer
  5. `review_comment_message` - Detailed review message written by the customer
  6. `review_creation_date` - Date when the review was created
  7. `review_answer_timestamp` - Timestamp when the seller answered the review
- **Data Quality**: ⚠️ Contains significant null values
  - `review_comment_title`: 87,656 (88.3%)
  - `review_comment_message`: 58,247 (58.7%)
- **Data Types**: 6 object columns, 1 integer column

### 6. Products Dataset
- **Shape**: 32,951 rows × 9 columns
- **Memory Usage**: 6.79 MB
- **Columns**: 
  1. `product_id` - Unique identifier for each product
  2. `product_category_name` - Category of the product in Portuguese
  3. `product_name_lenght` - Length of the product name in characters
  4. `product_description_lenght` - Length of the product description in characters
  5. `product_photos_qty` - Number of product photos available
  6. `product_weight_g` - Weight of the product in grams
  7. `product_length_cm` - Length of the product package in centimeters
  8. `product_height_cm` - Height of the product package in centimeters
  9. `product_width_cm` - Width of the product package in centimeters
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
  1. `seller_id` - Unique identifier for each seller
  2. `seller_zip_code_prefix` - First five digits of the seller's zip code
  3. `seller_city` - City where the seller is located
  4. `seller_state` - State where the seller is located
- **Data Quality**: ✅ No null values found
- **Data Types**: 3 object columns, 1 integer column

### 8. Geolocation Dataset
- **Shape**: 1,000,163 rows × 5 columns
- **Memory Usage**: 145.20 MB
- **Columns**: 
  1. `geolocation_zip_code_prefix` - First five digits of the zip code
  2. `geolocation_lat` - Latitude coordinate for the location
  3. `geolocation_lng` - Longitude coordinate for the location
  4. `geolocation_city` - City name corresponding to the zip code
  5. `geolocation_state` - State abbreviation corresponding to the zip code
- **Data Quality**: ✅ No null values found
- **Data Types**: 2 float columns, 2 object columns, 1 integer column

### 9. Category Translation Dataset
- **Shape**: 71 rows × 2 columns
- **Memory Usage**: 0.01 MB
- **Columns**: 
  1. `product_category_name` - Product category name in Portuguese
  2. `product_category_name_english` - Product category name translated to English
- **Data Quality**: ✅ No null values found
- **Data Types**: All 2 columns are object type

## Marketing Datasets

### 1. Marketing Qualified Leads Dataset
- **Shape**: 8,000 rows × 4 columns
- **Memory Usage**: 2.38 MB
- **Columns**: 
  1. `mql_id` - Unique identifier for each marketing qualified lead
  2. `first_contact_date` - Date of the first contact with the lead
  3. `landing_page_id` - Identifier for the landing page where the lead originated
  4. `origin` - Channel through which the lead was acquired (e.g., organic, paid, social)
- **Data Quality**: ⚠️ Contains minimal null values
  - `origin`: 60 (0.8%)
- **Data Types**: All 4 columns are object type

### 2. Closed Deals Dataset
- **Shape**: 842 rows × 14 columns
- **Memory Usage**: 0.65 MB
- **Columns**: 
  1. `mql_id` - Identifier linking to the marketing qualified lead
  2. `seller_id` - Unique identifier for the seller who closed the deal
  3. `sdr_id` - Identifier for the sales development representative
  4. `sr_id` - Identifier for the sales representative who closed the deal
  5. `won_date` - Date when the deal was successfully closed
  6. `business_segment` - Business segment classification of the closed deal
  7. `lead_type` - Type classification of the lead (e.g., new business, existing customer)
  8. `lead_behaviour_profile` - Behavioral profile classification of the lead
  9. `has_company` - Boolean indicator if the lead represents a company
  10. `has_gtin` - Boolean indicator if the lead has Global Trade Item Numbers
  11. `average_stock` - Average stock level declared by the lead
  12. `business_type` - Type of business model of the lead
  13. `declared_product_catalog_size` - Size of product catalog declared by the lead
  14. `declared_monthly_revenue` - Monthly revenue declared by the lead
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