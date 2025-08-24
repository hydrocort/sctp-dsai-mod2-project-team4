# Olist E-commerce Data Pipeline - Project Requirements Document (PRD)

## Project Overview

This project involves building an end-to-end data pipeline and analytics workflow for Brazilian e-commerce data from Olist. The pipeline will extract raw CSV data, load it into BigQuery, transform it into a star schema optimized for analytics, implement data quality validation, orchestrate all processes, and provide interactive dashboards for business insights.

## Business Questions to be Answered

The data pipeline and analytics solution must be capable of answering the following eight critical business questions:

1. **Monthly Sales Trends**: How do sales revenue, order volume, and average order values trend over time by month and year?

2. **Top Products and Categories**: Which product categories and individual products generate the highest revenue and sales volume?

3. **Geographic Sales Distribution**: How do sales vary across Brazilian regions, states, and cities for both customers and sellers?

4. **Customer Purchase Behavior**: What are the patterns in customer purchasing frequency, order values, and lifetime value across different customer segments?

5. **Payment Method Impact**: How do different payment methods (credit card, boleto, voucher) correlate with sales volumes and order values?

6. **Seller Performance Analysis**: Which sellers and regions perform best in terms of revenue generation, order fulfillment, and product diversity?

7. **Product Reviews and Sales Correlation**: How do customer review scores and review availability impact sales performance and customer behavior?

8. **Delivery Time Patterns**: What are the delivery performance metrics across regions, including on-time delivery rates and average delivery times?

## Detailed Star Schema Design

### Fact Table: FactSales

**Purpose**: Central fact table capturing each order item transaction with all relevant measures and dimensional context.

**Grain**: One record per order item (order_id + order_item_id combination)

| Column Name | Data Type | Description | Source/Transformation |
|-------------|-----------|-------------|----------------------|
| **Primary Key** |
| `order_item_sk` | STRING | Surrogate key for each order item | Generated: `CONCAT(order_id, '-', order_item_id)` |
| **Foreign Keys** |
| `order_key` | STRING | Reference to DimOrders | From `order_items.order_id` |
| `customer_key` | STRING | Reference to DimCustomers | From `orders.customer_id` via join on `order_items.order_id` |
| `product_key` | STRING | Reference to DimProducts | From `order_items.product_id` |
| `seller_key` | STRING | Reference to DimSellers | From `order_items.seller_id` |
| `date_key` | STRING | Reference to DimDate | From `orders.order_purchase_timestamp` (YYYY-MM-DD format) |
| `payment_key` | STRING | Reference to DimPayments | From `order_payments.order_id` via join |
| `review_key` | STRING | Reference to DimReviews (nullable) | From `order_reviews.order_id` via LEFT JOIN |
| **Measures** |
| `item_price` | NUMERIC | Price paid for the item | From `order_items.price` |
| `freight_value` | NUMERIC | Shipping cost for the item | From `order_items.freight_value` |
| `total_item_value` | NUMERIC | Total cost including shipping | Calculated: `price + freight_value` |
| `payment_value` | NUMERIC | Total payment amount for order | From `order_payments.payment_value` (aggregated if multiple payments) |
| `quantity` | INTEGER | Number of items | Static value of 1 per row |

### Dimension Tables

#### DimCustomers
| Column Name | Data Type | Source/Transformation |
|-------------|-----------|----------------------|
| `customer_key` | STRING | From `customers.customer_id` |
| `customer_unique_id` | STRING | From `customers.customer_unique_id` |
| `customer_city` | STRING | From `customers.customer_city` |
| `customer_state` | STRING | From `customers.customer_state` |
| `customer_zip_prefix` | STRING | From `customers.customer_zip_code_prefix` |
| `customer_region` | STRING | From `brazil_state_regions` seed via join on `customer_state` |

#### DimProducts
| Column Name | Data Type | Source/Transformation |
|-------------|-----------|----------------------|
| `product_key` | STRING | From `products.product_id` |
| `product_category_portuguese` | STRING | From `products.product_category_name` |
| `product_category_english` | STRING | From `category_translation.product_category_name_english` via join |
| `product_weight_g` | NUMERIC | From `products.product_weight_g` |
| `product_length_cm` | NUMERIC | From `products.product_length_cm` |
| `product_height_cm` | NUMERIC | From `products.product_height_cm` |
| `product_width_cm` | NUMERIC | From `products.product_width_cm` |
| `product_volume_cm3` | NUMERIC | Calculated: `length * height * width` (with null handling) |
| `product_photos_qty` | INTEGER | From `products.product_photos_qty` |
| `product_name_length` | INTEGER | From `products.product_name_lenght` |
| `product_description_length` | INTEGER | From `products.product_description_lenght` |

#### DimSellers
| Column Name | Data Type | Source/Transformation |
|-------------|-----------|----------------------|
| `seller_key` | STRING | From `sellers.seller_id` |
| `seller_city` | STRING | From `sellers.seller_city` |
| `seller_state` | STRING | From `sellers.seller_state` |
| `seller_zip_prefix` | STRING | From `sellers.seller_zip_code_prefix` |
| `seller_region` | STRING | From `brazil_state_regions` seed via join on `seller_state` |

#### DimDate
| Column Name | Data Type | Source/Transformation |
|-------------|-----------|----------------------|
| `date_key` | STRING | From `orders.order_purchase_timestamp` (YYYY-MM-DD format) |
| `full_date` | DATE | From `orders.order_purchase_timestamp` |
| `year` | INTEGER | Extracted from `order_purchase_timestamp` |
| `month` | INTEGER | Extracted from `order_purchase_timestamp` |
| `month_name` | STRING | Derived from month number |
| `quarter` | INTEGER | Calculated from month |
| `day_of_week` | INTEGER | Extracted from `order_purchase_timestamp` |
| `day_name` | STRING | Derived from day_of_week |
| `is_weekend` | BOOLEAN | Calculated from day_of_week |

#### DimOrders
| Column Name | Data Type | Source/Transformation |
|-------------|-----------|----------------------|
| `order_key` | STRING | From `orders.order_id` |
| `order_status` | STRING | From `orders.order_status` |
| `order_purchase_timestamp` | TIMESTAMP | From `orders.order_purchase_timestamp` |
| `order_approved_at` | TIMESTAMP | From `orders.order_approved_at` |
| `order_delivered_carrier_date` | TIMESTAMP | From `orders.order_delivered_carrier_date` |
| `order_delivered_customer_date` | TIMESTAMP | From `orders.order_delivered_customer_date` |
| `order_estimated_delivery_date` | TIMESTAMP | From `orders.order_estimated_delivery_date` |
| `days_to_delivery` | INTEGER | Calculated: `DATE_DIFF(order_delivered_customer_date, order_purchase_timestamp, DAY)` |
| `delivery_vs_estimate_days` | INTEGER | Calculated: `DATE_DIFF(order_delivered_customer_date, order_estimated_delivery_date, DAY)` |
| `is_delivered_on_time` | BOOLEAN | Calculated: `delivery_vs_estimate_days <= 0` |

#### DimPayments
| Column Name | Data Type | Source/Transformation |
|-------------|-----------|----------------------|
| `payment_key` | STRING | From `order_payments.order_id` (one record per order) |
| `primary_payment_type` | STRING | Most frequent `payment_type` for the order via aggregation |
| `total_installments` | INTEGER | Sum of `payment_installments` for the order |
| `payment_methods_count` | INTEGER | Count of distinct payment methods used per order |
| `uses_credit_card` | BOOLEAN | Whether order used credit card payment |
| `uses_boleto` | BOOLEAN | Whether order used boleto payment |
| `uses_voucher` | BOOLEAN | Whether order used voucher payment |

#### DimReviews
| Column Name | Data Type | Source/Transformation |
|-------------|-----------|----------------------|
| `review_key` | STRING | From `order_reviews.order_id` |
| `review_score` | INTEGER | From `order_reviews.review_score` |
| `has_comment_title` | BOOLEAN | Whether `review_comment_title` is not null |
| `has_comment_message` | BOOLEAN | Whether `review_comment_message` is not null |
| `review_creation_date` | TIMESTAMP | From `order_reviews.review_creation_date` |
| `days_to_review` | INTEGER | Calculated: `DATE_DIFF(review_creation_date, order_purchase_timestamp, DAY)` |

### Seed Tables

#### brazil_state_regions
| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `state_code` | STRING | Two-letter Brazilian state code |
| `state_name` | STRING | Full state name |
| `region` | STRING | Brazilian geographic region (North, Northeast, Southeast, South, Central-West) |
| `economic_zone` | STRING | Economic classification zone |

Complete seed data includes all 27 Brazilian states plus Federal District covering: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SP, SE, TO.

#### Create the Seed File

```csv
# seeds/brazil_state_regions.csv
state_code,state_name,region,economic_zone
AC,Acre,North,Amazon
AL,Alagoas,Northeast,Northeast
AP,Amapá,North,Amazon
AM,Amazonas,North,Amazon
BA,Bahia,Northeast,Northeast
CE,Ceará,Northeast,Northeast
DF,Distrito Federal,Central-West,Central
ES,Espírito Santo,Southeast,Southeast
GO,Goiás,Central-West,Central
MA,Maranhão,Northeast,Northeast
MT,Mato Grosso,Central-West,Central
MS,Mato Grosso do Sul,Central-West,Central
MG,Minas Gerais,Southeast,Southeast
PA,Pará,North,Amazon
PB,Paraíba,Northeast,Northeast
PR,Paraná,South,South
PE,Pernambuco,Northeast,Northeast
PI,Piauí,Northeast,Northeast
RJ,Rio de Janeiro,Southeast,Southeast
RN,Rio Grande do Norte,Northeast,Northeast
RS,Rio Grande do Sul,South,South
RO,Rondônia,North,Amazon
RR,Roraima,North,Amazon
SC,Santa Catarina,South,South
SP,São Paulo,Southeast,Southeast
SE,Sergipe,Northeast,Northeast
TO,Tocantins,North,Amazon
```

#### Configure the Seed

```yaml
# dbt_project.yml
seeds:
  your_project_name:
    brazil_state_regions:
      +column_types:
        state_code: string
        state_name: string
        region: string
        economic_zone: string
```

## How Schema Answers Business Questions

1. **Monthly Sales Trends**: DimDate (year, month, month_name) + FactSales measures (total_item_value, payment_value)
2. **Top Products/Categories**: DimProducts (product_category_english) + FactSales aggregations
3. **Geographic Sales Distribution**: DimCustomers.customer_region + DimSellers.seller_region + FactSales measures
4. **Customer Purchase Behavior**: DimCustomers + FactSales (frequency via COUNT, value via SUM)
5. **Payment Method Impact**: DimPayments (primary_payment_type, payment flags) + FactSales measures
6. **Seller Performance**: DimSellers + FactSales aggregations by seller and region
7. **Reviews Correlation**: DimReviews.review_score + FactSales measures (with null handling for missing reviews)
8. **Delivery Patterns**: DimOrders delivery metrics + DimDate for temporal analysis + DimCustomers for regional patterns

## Key Schema Design Decisions

### Grain Selection
- **Fact Table Grain**: Order item level (not order level) to maintain granular product-level analysis while supporting order-level aggregation

### Slowly Changing Dimensions
- **Type 1 (Overwrite)**: All dimensions use Type 1 SCD since dataset is historical, not live operational data

### Null Handling Strategy
- **Reviews**: Use LEFT JOIN in fact table allowing `review_key` to be NULL when no review exists, maintaining semantic accuracy between missing reviews and actual zero-star reviews

### Derived Attributes Implementation
- **Delivery Performance**: Calculate delivery metrics (days_to_delivery, is_delivered_on_time) in DimOrders
- **Regional Groupings**: Use dbt seed for Brazilian state-to-region mapping via joins
- **Payment Behavior**: Aggregate payment methods per order in DimPayments with boolean flags
- **Product Dimensions**: Calculate volume and enrich with English category names


## Detailed Transformation Requirements

### Staging Layer Transformations
- **Data Type Conversion**: Cast numeric fields from STRING to appropriate numeric types
- **Date Parsing**: Convert timestamp strings to TIMESTAMP data types
- **Data Cleaning**: Trim whitespace, standardize case for text fields
- **Column Renaming**: Standardize naming conventions across all tables
- **Null Standardization**: Handle various null representations consistently

### Marts Layer Transformations

#### Derived Attributes Implementation

**Regional Groupings via Seed**:
```sql
-- Join customers/sellers with seed for regional classification
LEFT JOIN {{ ref('brazil_state_regions') }} r
    ON customer_state = r.state_code
```

**Delivery Performance Calculations**:
```sql
-- Calculate delivery metrics in DimOrders
DATE_DIFF(
    DATE(order_delivered_customer_date), 
    DATE(order_purchase_timestamp), 
    DAY
) as days_to_delivery

CASE 
    WHEN DATE_DIFF(
        DATE(order_delivered_customer_date), 
        DATE(order_estimated_delivery_date), 
        DAY
    ) <= 0 THEN TRUE
    ELSE FALSE
END as is_delivered_on_time
```

**Payment Aggregation**:
```sql
-- Aggregate payment methods per order in DimPayments
MAX(CASE WHEN payment_type = 'credit_card' THEN TRUE ELSE FALSE END) as uses_credit_card
```

**Product Volume Calculation**:
```sql
-- Calculate product volume with null handling
COALESCE(
    product_length_cm * product_height_cm * product_width_cm, 
    0
) as product_volume_cm3
```

### Null Handling for Reviews

**Implementation Strategy**: Use LEFT JOIN in FactSales to preserve orders without reviews:

```sql
FROM {{ ref('stg_order_items') }} oi
-- Other INNER JOINs...
LEFT JOIN {{ ref('dim_reviews') }} r  -- LEFT JOIN allows nulls
    ON oi.order_id = r.review_key
```

**Analytics Handling**: Distinguish between missing reviews and actual ratings in analysis queries:
```sql
CASE 
    WHEN r.review_key IS NULL THEN 'No Review'
    WHEN r.review_score >= 4 THEN 'Positive'
    WHEN r.review_score = 3 THEN 'Neutral' 
    ELSE 'Negative'
END as review_category
```

## Complete Project Flow

```
[CSV Files] → [Meltano Extraction & Loading] → [BigQuery Raw Dataset] → [Great Expectations Raw Validation] → [dbt Staging Transformation] → [dbt Marts Transformation] → [Great Expectations Marts Validation] → [BigQuery Marts Dataset] → [Streamlit Dashboard Analytics]

All orchestrated and monitored by Dagster
```

## Detailed BigQuery Project Structure

```
your-gcp-project-id/
├── olist_raw/                          # Raw data landing zone
│   ├── raw_customers                   # Direct CSV load via Meltano
│   ├── raw_orders                      # Direct CSV load via Meltano  
│   ├── raw_order_items                 # Direct CSV load via Meltano
│   ├── raw_order_payments              # Direct CSV load via Meltano
│   ├── raw_order_reviews               # Direct CSV load via Meltano
│   ├── raw_products                    # Direct CSV load via Meltano
│   ├── raw_sellers                     # Direct CSV load via Meltano
│   ├── raw_geolocation                 # Direct CSV load via Meltano
│   └── raw_category_translation        # Direct CSV load via Meltano
│
├── olist_staging/                      # Cleaned and typed data
│   ├── stg_customers                   # dbt staging model
│   ├── stg_orders                      # dbt staging model
│   ├── stg_order_items                 # dbt staging model
│   ├── stg_order_payments              # dbt staging model
│   ├── stg_order_reviews               # dbt staging model
│   ├── stg_products                    # dbt staging model
│   ├── stg_sellers                     # dbt staging model
│   ├── stg_geolocation                 # dbt staging model
│   └── stg_category_translation        # dbt staging model
│
└── olist_marts/                        # Analytics-ready star schema
    ├── dim_customers                   # Customer dimension
    ├── dim_products                    # Product dimension
    ├── dim_sellers                     # Seller dimension
    ├── dim_orders                      # Order dimension
    ├── dim_payments                    # Payment dimension
    ├── dim_reviews                     # Review dimension
    ├── dim_date                        # Date dimension
    ├── fact_sales                      # Central fact table
    └── brazil_state_regions            # Reference seed data
```
### Data Architecture
- **Single Mart Approach**: All star schema objects in `olist_marts` dataset for simplified management and unified analytics

## Stage-by-Stage Overview

### Raw Layer (olist_raw)
**Purpose**: Landing zone for exact CSV file contents
**Characteristics**:
- Unchanged data from source CSV files
- All columns stored as STRING data type
- Includes Meltano metadata columns (_sdc_extracted_at, _sdc_table_version)
- Preserves original data quality issues for auditing
- No business logic applied

**Achievement**: Reliable, auditable copy of source data in cloud data warehouse

### Staging Layer (olist_staging)  
**Purpose**: Clean and prepare raw data for business logic
**Transformations**:
- Convert data types from STRING to appropriate types (INTEGER, NUMERIC, TIMESTAMP, BOOLEAN)
- Standardize text fields (trim whitespace, normalize case)
- Parse and validate timestamp formats
- Remove Meltano metadata columns not needed for analysis
- Apply basic data quality filters (remove records with null primary keys)
- Rename columns to follow consistent naming conventions

**Achievement**: Type-safe, clean data ready for dimensional modeling

### Marts Layer (olist_marts)
**Purpose**: Business-ready analytical data warehouse
**Transformations**:
- Implement star schema dimensional model
- Create calculated fields and derived metrics
- Join tables to enrich data with business context
- Apply complex business rules and logic
- Aggregate data where appropriate (payment methods per order)
- Implement proper foreign key relationships

**Achievement**: Optimized analytical data warehouse supporting all business questions with fast query performance

## Great Expectations Integration Points

### 1. Post-Ingestion Validation (Raw Layer)
**Timing**: After Meltano completes data loading into BigQuery Raw
**Purpose**: Ensure data extraction and loading completed successfully with expected quality

**Raw Data Validations**:

**Structural Validations**:
- `ExpectTableToExist()` - Verify all expected tables were created
- `ExpectTableColumnCountToEqual()` - Validate correct number of columns per table
- `ExpectColumnToExist()` - Confirm critical columns are present
- `ExpectTableRowCountToBeBetween()` - Check row counts within expected ranges

**Data Quality Validations**:
- `ExpectColumnValuesToNotBeNull()` - Validate primary keys (customer_id, order_id, product_id, seller_id) are populated
- `ExpectColumnValuesToBeUnique()` - Ensure primary key uniqueness
- `ExpectColumnValuesToBeInSet()` - Validate Brazilian state codes against known values
- `ExpectColumnValuesToMatchRegex()` - Validate ID formats and zip code patterns
- `ExpectColumnValuesToBeBetween()` - Check numeric fields for reasonable ranges (prices > 0)

**Business Logic Validations**:
- Order dates should be within expected business operation timeframe
- Product weights and dimensions should be positive values
- Review scores should be between 1 and 5
- Payment values should be positive

### 2. Post-Transformation Validation (Marts Layer)
**Timing**: After dbt completes marts transformation
**Purpose**: Validate business logic implementation and analytical data quality

**Business Logic Validations**:
- `ExpectColumnPairValuesToBeEqual()` - Verify total_item_value equals item_price + freight_value
- `ExpectColumnValuesToBePositive()` - Ensure all monetary values are positive
- `ExpectColumnSumToBeBetween()` - Validate aggregated totals are within expected ranges

**Referential Integrity Validations**:
- `ExpectColumnValuesToNotBeNull()` - All foreign keys except review_key must be populated
- Foreign key values must exist in corresponding dimension tables
- Date keys must exist in DimDate table

**Data Completeness Validations**:
- All order items should have corresponding payment records
- Customer and seller regional assignments should be complete
- Product category translations should be available for all products

**Analytical Consistency Validations**:
- Monthly sales totals should show reasonable business patterns
- Regional distributions should align with Brazilian geography
- Delivery time calculations should be logical (positive days, reasonable ranges)

## Dagster Integration Points

### Dagster Asset Structure
**Purpose**: Define dependencies, monitor execution, and provide data lineage visibility

**Ingestion Assets**:
- `meltano_extract_load`: Execute Meltano pipeline to load CSV files into BigQuery raw tables
- `validate_raw_customers`: Run Great Expectations validation on raw customer data  
- `validate_raw_orders`: Run Great Expectations validation on raw order data
- `validate_raw_products`: Run Great Expectations validation on raw product data
- `validate_raw_sellers`: Run Great Expectations validation on raw seller data
- `validate_raw_payments`: Run Great Expectations validation on raw payment data
- `validate_raw_reviews`: Run Great Expectations validation on raw review data

**Transformation Assets**:
- `dbt_staging_models`: Execute dbt models for staging layer (depends on raw validation assets)
- `dbt_marts_models`: Execute dbt models for marts layer (depends on staging completion)

**Quality Assurance Assets**:
- `validate_fact_sales`: Run Great Expectations validation on fact table
- `validate_dim_customers`: Run Great Expectations validation on customer dimension
- `validate_dim_products`: Run Great Expectations validation on product dimension
- `validate_dim_sellers`: Run Great Expectations validation on seller dimension
- `validate_dim_orders`: Run Great Expectations validation on order dimension
- `validate_dim_payments`: Run Great Expectations validation on payment dimension
- `validate_dim_reviews`: Run Great Expectations validation on review dimension

**Analytics Assets**:
- `streamlit_dashboard_refresh`: Signal dashboard data refresh completion

### Dagster Orchestration Responsibilities

**Dependency Management**:
- Ensure raw data validation completes before starting dbt staging transformations
- Prevent marts transformation until all staging models complete successfully
- Block dashboard refresh until all marts validations pass

**Error Handling and Alerting**:
- Stop pipeline execution if critical validations fail
- Send notifications for data quality issues requiring attention
- Implement retry logic for transient failures
- Provide detailed failure context and debugging information

**Monitoring and Observability**:
- Track execution time for each pipeline step
- Monitor resource utilization (BigQuery slots, compute usage)
- Maintain historical run logs and performance metrics
- Provide data lineage visualization

**Scheduling and Triggering**:
- Schedule daily pipeline execution
- Support manual pipeline triggers for ad-hoc runs
- Enable partial pipeline re-runs from specific points

## Streamlit Requirements

### Authentication Requirements
**Method**: Google Cloud Service Account authentication
**Implementation**: Service account credentials stored in Streamlit secrets management
**Permissions Required**:
- BigQuery Data Viewer role on olist_marts dataset
- BigQuery Job User role for query execution
- Access limited to analytical queries (no write permissions)

### Data Fetching Functions

**Core Query Functions Required**:
- `get_monthly_sales_trends()`: Aggregate sales metrics by month/year from FactSales + DimDate
- `get_top_products_categories()`: Product performance analysis from FactSales + DimProducts  
- `get_sales_by_region()`: Geographic analysis from FactSales + DimCustomers + DimSellers
- `get_customer_behavior()`: Customer analytics from FactSales + DimCustomers aggregations
- `get_payment_analysis()`: Payment method impact from FactSales + DimPayments
- `get_seller_performance()`: Seller metrics from FactSales + DimSellers
- `get_reviews_sales_correlation()`: Review impact analysis from FactSales + DimReviews (with null handling)
- `get_delivery_patterns()`: Delivery analytics from FactSales + DimOrders + regional dimensions

**Technical Requirements**:
- Implement `@st.cache_data(ttl=600)` for query result caching (10-minute cache)
- BigQuery client connection pooling for performance
- Error handling for failed queries with user-friendly messages
- Query timeout management for long-running analytical queries

### Dashboard Structure Requirements

**Multi-Tab Interface**:
- 8 dedicated tabs corresponding to each business question
- Sidebar controls for data refresh and filtering options
- Responsive layout supporting both desktop and mobile viewing

**Visualization Components**:
- Interactive Plotly charts for trend analysis, geographic distributions, and performance metrics
- Data tables with sorting and filtering capabilities  
- Key performance indicator (KPI) metric displays
- Dynamic filtering and drill-down capabilities

**User Experience Features**:
- Manual data refresh button to clear cache
- Loading indicators for query execution
- Export capabilities for charts and data
- Responsive design for various screen sizes

### Streamlit Project Structure

```
streamlit_dashboard/
├── streamlit_app.py                    # Main application entry point
├── .streamlit/
│   ├── config.toml                     # Streamlit configuration
│   └── secrets.toml                    # GCP service account credentials
├── utils/
│   ├── bigquery_client.py              # BigQuery connection management
│   ├── data_queries.py                 # Business question query functions
│   └── visualization_helpers.py        # Chart generation utilities
├── pages/
│   └── data_explorer.py                # Additional analytical pages
├── requirements.txt                    # Python dependencies
├── README.md                          # Setup and deployment instructions
└── .gitignore                         # Exclude secrets from version control
```

### Deployment Requirements

**Streamlit Cloud Deployment**:
- GitHub repository integration for automatic deployments
- Secrets management through Streamlit Cloud dashboard (GCP service account JSON)
- Custom domain configuration capability
- SSL certificate management

**Local Development Support**:
- Docker containerization option for consistent development environment
- Environment variable management for local GCP authentication
- Development/production configuration separation

**Performance Requirements**:
- Initial page load under 3 seconds
- Query response time under 10 seconds for complex analytics
- Support for concurrent users (estimated 10-50 simultaneous users)
- Graceful handling of BigQuery quota limits

**Security Requirements**:
- No hardcoded credentials in source code
- Secure service account key management
- Read-only database access permissions
- User session management and timeout handling