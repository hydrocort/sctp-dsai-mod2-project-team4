# Dataset Overview - E-commerce Marketing Analytics

## Executive Summary

This document provides a comprehensive overview of the datasets used in our e-commerce marketing analytics project. The data consists of **11 datasets** split into two main categories:
- **9 E-commerce datasets** containing marketplace transaction data
- **2 Marketing datasets** containing lead generation and conversion data

---

## E-commerce Datasets

### 1. Customers Dataset
- **Shape**: 99,441 rows × 5 columns
- **Memory Usage**: 29.62 MB
- **Data Quality**: ✅ No null values
- **Key Columns**:
  - `customer_id` - Unique customer identifier
  - `customer_unique_id` - Business key for customer
  - `customer_zip_code_prefix` - Geographic location
  - `customer_city` - Customer city
  - `customer_state` - Customer state

### 2. Orders Dataset
- **Shape**: 99,441 rows × 8 columns
- **Memory Usage**: 58.97 MB
- **Data Quality**: ⚠️ Some null values in delivery dates
- **Key Columns**:
  - `order_id` - Unique order identifier
  - `customer_id` - Links to customers
  - `order_status` - Order lifecycle status
  - `order_purchase_timestamp` - Purchase date/time
- **Missing Data**:
  - `order_approved_at`: 160 records (0.2%)
  - `order_delivered_carrier_date`: 1,783 records (1.8%)
  - `order_delivered_customer_date`: 2,965 records (3.0%)

### 3. Order Items Dataset
- **Shape**: 112,650 rows × 7 columns
- **Memory Usage**: 39.43 MB
- **Data Quality**: ✅ No null values
- **Key Columns**:
  - `order_id` - Links to orders
  - `product_id` - Links to products
  - `seller_id` - Links to sellers
  - `price` - Item price
  - `freight_value` - Shipping cost

### 4. Order Payments Dataset
- **Shape**: 103,886 rows × 5 columns
- **Memory Usage**: 17.81 MB
- **Data Quality**: ✅ No null values
- **Key Columns**:
  - `order_id` - Links to orders
  - `payment_type` - Payment method
  - `payment_installments` - Number of installments
  - `payment_value` - Payment amount

### 5. Order Reviews Dataset
- **Shape**: 99,224 rows × 7 columns
- **Memory Usage**: 42.75 MB
- **Data Quality**: ⚠️ High percentage of missing review content
- **Key Columns**:
  - `review_id` - Unique review identifier
  - `order_id` - Links to orders
  - `review_score` - Rating (1-5 scale)
- **Missing Data**:
  - `review_comment_title`: 87,656 records (88.3%)
  - `review_comment_message`: 58,247 records (58.7%)

### 6. Products Dataset
- **Shape**: 32,951 rows × 9 columns
- **Memory Usage**: 6.79 MB
- **Data Quality**: ⚠️ Some missing product attributes
- **Key Columns**:
  - `product_id` - Unique product identifier
  - `product_category_name` - Product category
  - Physical dimensions and weight attributes
- **Missing Data**:
  - Product attributes: 610 records (1.9%) missing across multiple fields
  - Physical dimensions: 2 records (0.0%) missing

### 7. Sellers Dataset
- **Shape**: 3,095 rows × 4 columns
- **Memory Usage**: 0.66 MB
- **Data Quality**: ✅ No null values
- **Key Columns**:
  - `seller_id` - Unique seller identifier
  - Geographic location attributes

### 8. Geolocation Dataset
- **Shape**: 1,000,163 rows × 5 columns
- **Memory Usage**: 145.20 MB
- **Data Quality**: ✅ No null values
- **Key Columns**:
  - `geolocation_zip_code_prefix` - ZIP code
  - `geolocation_lat` / `geolocation_lng` - Coordinates
  - City and state information

### 9. Category Translation Dataset
- **Shape**: 71 rows × 2 columns
- **Memory Usage**: 0.01 MB
- **Data Quality**: ✅ No null values
- **Purpose**: Maps Portuguese category names to English

---

## Marketing Datasets

### 1. Marketing Qualified Leads (MQLs)
- **Shape**: 8,000 rows × 4 columns
- **Memory Usage**: 2.38 MB
- **Data Quality**: ⚠️ Minimal missing data
- **Key Columns**:
  - `mql_id` - Unique lead identifier
  - `first_contact_date` - Initial touchpoint date
  - `landing_page_id` - Entry point tracking
  - `origin` - Marketing channel source
- **Missing Data**:
  - `origin`: 60 records (0.8%)

### 2. Closed Deals
- **Shape**: 842 rows × 14 columns
- **Memory Usage**: 0.65 MB
- **Data Quality**: ⚠️ High percentage of missing business details
- **Key Columns**:
  - `mql_id` - Links to marketing leads
  - `seller_id` - Links to e-commerce sellers
  - `won_date` - Deal closure date
  - `business_segment` / `business_type` - Business classification
- **Missing Data** (High missing rates for business details):
  - `has_company`: 779 records (92.5%)
  - `has_gtin`: 778 records (92.4%)
  - `average_stock`: 776 records (92.2%)
  - `declared_product_catalog_size`: 773 records (91.8%)

---

## Data Integration Points

### Primary Linkages
1. **E-commerce ↔ Marketing**: `seller_id` connects closed deals to e-commerce transactions
2. **Orders ↔ Customers**: `customer_id` links customer demographics to purchase behavior
3. **Orders ↔ Products**: `product_id` connects transactions to product attributes
4. **Geographic**: ZIP codes link customers/sellers to precise coordinates

### Data Quality Assessment

| Dataset Category | Overall Quality | Key Issues |
|------------------|-----------------|------------|
| **E-commerce Core** | 🟢 **Excellent** | Minimal missing data in transaction tables |
| **E-commerce Reviews** | 🟡 **Good** | High missing rate in review content (88% titles) |
| **Marketing Leads** | 🟢 **Excellent** | Only 0.8% missing channel attribution |
| **Marketing Deals** | 🟡 **Limited** | 90%+ missing business profile data |

### Total Dataset Size
- **Combined Memory Usage**: ~343 MB
- **Total Records**: ~1.4M+ across all datasets
- **Primary Analysis Focus**: 99K+ orders with 112K+ line items from 3K+ sellers