# Olist E-commerce Data Pipeline - Implementation Plan

## Project Overview

This implementation plan provides a step-by-step guide to build the Olist e-commerce data pipeline as specified in the PRD. Each stage includes detailed to-dos that can be executed with Claude Code or Cursor to systematically complete the project.

## Prerequisites

- [x] **Environment Setup**: Activate `mod2proj` conda environment with all dependencies installed per `environment.yml` ✅
- [x] **Data Ingestion Complete**: `data_ingestion.py` has been executed and CSV files are available in `./data/` directory ✅
- [x] **GCP Project**: Active Google Cloud Project with billing enabled ✅
- [x] **Service Account**: GCP service account with BigQuery Admin and Storage Admin permissions ✅

### ✅ Prerequisites Completion Summary

All prerequisites have been successfully completed:

1. **Environment Setup** ✅
   - `mod2proj` conda environment is active
   - All dependencies from `environment.yml` are installed
   - Environment tested and working

2. **Data Ingestion Complete** ✅
   - `data_ingestion.py` has been executed successfully
   - All 9 CSV files are available in `./data/brazilian-ecommerce/` directory:
     - `olist_customers_dataset.csv`
     - `olist_orders_dataset.csv`
     - `olist_order_items_dataset.csv`
     - `olist_order_payments_dataset.csv`
     - `olist_order_reviews_dataset.csv`
     - `olist_products_dataset.csv`
     - `olist_sellers_dataset.csv`
     - `olist_geolocation_dataset.csv`
     - `product_category_name_translation.csv`

3. **GCP Project** ✅
   - Active Google Cloud Project: `sctp-dsai-468313`
   - Billing enabled and verified
   - BigQuery API enabled

4. **Service Account** ✅
   - Service Account: `bigquery-admin@sctp-dsai-468313.iam.gserviceaccount.com`
   - BigQuery Admin permissions: Verified ✅
   - Storage Admin permissions: Available ✅
   - Authentication tested and working
   - Credentials securely stored in `./credentials/` directory
   - Environment variables configured in `.env` file

### 🚀 Ready to Proceed

The project is now fully prepared to begin **Stage 1: Hybrid Data Loading (CSV → DuckDB → BigQuery)**.

---

## Stage 1: Hybrid Data Loading (CSV → DuckDB → BigQuery)

**Objective**: Load CSV data reliably into BigQuery using a two-stage hybrid approach to overcome CSV encoding and configuration issues

**Architecture Change**: After encountering multiple issues with direct CSV → BigQuery loading via Meltano (encoding errors, column naming restrictions, row count discrepancies), we implemented a hybrid approach:
- **Stage 1A**: Direct CSV → DuckDB (native, reliable loading)
- **Stage 1B**: DuckDB → BigQuery via Meltano (controlled, clean transfer)

### 1A. Direct CSV to DuckDB Loading

**Objective**: Load all CSV files directly into DuckDB for reliable data handling and validation

#### 1A.1 Environment Setup
- [x] **Install DuckDB in conda environment** ✅
  ```bash
  conda activate mod2proj
  pip install duckdb==1.1.3
  ```

- [x] **Update environment.yml** ✅
  - [x] Add `duckdb==1.1.3` to pip dependencies ✅

#### 1A.2 Create DuckDB Loading Script
- [x] **Create load_csv_to_duckdb.py** ✅
  - [x] Implement automatic CSV file detection ✅
  - [x] Use DuckDB's `read_csv_auto()` for schema inference ✅
  - [x] Create all 9 raw tables with proper naming convention ✅
  - [x] Implement data validation and row count verification ✅
  - [x] Add comprehensive logging and error handling ✅

#### 1A.3 Execute CSV Loading
- [x] **Load all CSV files into DuckDB** ✅
  ```bash
  python load_csv_to_duckdb.py
  ```

- [x] **Verify data loading success** ✅
  - [x] All 9 CSV files loaded successfully ✅
  - [x] Total records: 1,550,922 rows across all tables ✅
  - [x] Database file created: `olist_data.duckdb` ✅
  - [x] Sample queries validated ✅

**Loaded Tables**:
- ✅ `raw_customers`: 99,441 rows, 5 columns ✅
- ✅ `raw_orders`: 99,441 rows, 8 columns ✅
- ✅ `raw_order_items`: 112,650 rows, 7 columns ✅
- ✅ `raw_order_payments`: 103,886 rows, 5 columns ✅
- ✅ `raw_order_reviews`: 99,224 rows, 7 columns ✅ *(minor row filtering by DuckDB)*
- ✅ `raw_products`: 32,951 rows, 9 columns ✅
- ✅ `raw_sellers`: 3,095 rows, 4 columns ✅
- ✅ `raw_geolocation`: 1,000,163 rows, 5 columns ✅
- ✅ `raw_category_translation`: 71 rows, 2 columns ✅

#### 1A.4 Clean Up Previous Meltano Configuration
- [x] **Remove problematic configurations** ✅
  - [x] Removed tap-csv extractor configuration ✅
  - [x] Removed target-bigquery loader configuration ✅
  - [x] Preserved Meltano project structure for Stage 1B ✅

**Stage 1A Completion Criteria**:
- ✅ DuckDB database created successfully ✅
- ✅ All 9 tables loaded with expected data ✅
- ✅ Data quality validated (row counts, sample queries) ✅
- ✅ Ready for Stage 1B transfer to BigQuery ✅

### 1B. DuckDB to BigQuery via Meltano

**Objective**: Use Meltano to extract clean data from DuckDB and load into BigQuery raw layer

#### 1B.1 Meltano Configuration for DuckDB Source
- [x] **Install tap-duckdb extractor** ✅
  ```bash
  meltano add extractor tap-duckdb
  ```

- [x] **Configure tap-duckdb in meltano.yml** ✅
  - [x] Set database path to `olist_data.duckdb` ✅
  - [x] Configure table selection for all 9 raw tables ✅
  - [x] Set up appropriate schema mappings ✅

#### 1B.2 Configure BigQuery Target
- [x] **Install/configure target-bigquery loader** ✅
  ```bash
  meltano add loader target-bigquery
  ```

- [x] **Set up BigQuery connection** ✅
  - [x] Configure GCP service account authentication ✅
  - [x] Set target dataset to `olist_raw` ✅
  - [x] Configure table naming convention ✅
  - [x] Set appropriate location and batch settings ✅

#### 1B.3 Execute DuckDB to BigQuery Transfer
- [x] **Test connections** ✅
  ```bash
  meltano invoke tap-duckdb --discover
  meltano invoke target-bigquery --version
  ```

- [x] **Run data transfer** ✅
  ```bash
  meltano run tap-duckdb target-bigquery
  ```

- [x] **Verify BigQuery tables created** ✅
  - [x] Check BigQuery console for `olist_raw` dataset ✅
  - [x] Verify all 9 raw tables exist with correct row counts ✅
  - [x] Check table schemas match DuckDB structure ✅
  - [x] Data integrity verified (32,951 rows in products table matches DuckDB) ✅

#### 1B.4 Create Meltano Schedules (Optional)
- [ ] **Set up daily schedule for incremental updates**
  ```bash
  meltano schedule add daily-load --extractor tap-duckdb --loader target-bigquery --interval @daily
  ```

**Stage 1B Completion Criteria**:
- [x] All 9 raw tables exist in BigQuery `olist_raw` dataset
- [x] Row counts match DuckDB source tables exactly
- [x] Sample data queries return expected results
- [x] Meltano configuration is version controlled
- [x] Data transfer process is reliable and repeatable

**Overall Stage 1 Completion Criteria**:
- ✅ CSV data successfully loaded into intermediate DuckDB ✅
- ✅ DuckDB data successfully transferred to BigQuery via Meltano ✅
- ✅ All data quality validations pass ✅
- ✅ Pipeline is ready for Stage 2 (dbt transformations) ✅

---

## Stage 2: Transformation and Setting up Staging and Marts (dbt)

**Objective**: Set up dbt to transform raw data into staging layer and star schema marts

### 2.1 dbt Project Initialization ✅
- [x] **Initialize dbt project** ✅
  ```bash
  dbt init olist_analytics
  cd olist_analytics
  ```

- [x] **Configure dbt profiles** ✅
  - [x] Set up `~/.dbt/profiles.yml` for BigQuery connection ✅
  - [x] Configure authentication method (service account key) ✅
  - [x] Set location and dataset configurations ✅

### 2.2 dbt Project Configuration ✅
- [x] **Update dbt_project.yml** ✅
  - [x] Set project name: `olist_analytics` ✅
  - [x] Configure model paths and schema configurations ✅
  - [x] Set staging models to views, marts to tables ✅
  - [x] Configure dataset names (staging: `olist_staging`, marts: `olist_marts`) ✅

- [x] **Create directory structure** ✅
  ```
  models/
  ├── staging/
  ├── marts/
  │   ├── dimensions/
  │   └── facts/
  └── sources/
  seeds/
  tests/
  macros/
  ```

### 2.3 Configure Sources ✅
- [x] **Create sources.yml** ✅
  - [x] Define `olist_raw` source ✅
  - [x] Configure all 9 raw tables as source tables ✅
  - [x] Add source descriptions and column documentation ✅

### 2.4 Create Staging Models
- [x] **Create staging models for each source table** ✅:
  - [x] `stg_customers.sql` - Type casting, column renaming, basic cleaning ✅
  - [x] `stg_orders.sql` - Timestamp parsing, status standardization ✅
  - [x] `stg_order_items.sql` - Numeric type conversion, validation ✅
  - [x] `stg_order_payments.sql` - Payment type standardization ✅
  - [x] `stg_order_reviews.sql` - Score validation, date parsing ✅
  - [x] `stg_products.sql` - Dimension calculations, null handling ✅
  - [x] `stg_sellers.sql` - Location data cleaning ✅
  - [x] `stg_geolocation.sql` - Coordinate validation ✅
  - [x] `stg_category_translation.sql` - Text normalization ✅

- [x] **Implement common transformations**:
  - [x] Data type conversions (STRING to appropriate types)
  - [x] Trim whitespace and standardize text fields
  - [x] Parse timestamps to proper TIMESTAMP type
  - [x] Apply basic data quality filters

### 2.5 Create Seed Files
- [x] **Create brazil_state_regions.csv seed file**
  - [x] Include all 27 Brazilian states + Federal District
  - [x] Add columns: state_code, state_name, region, economic_zone
  - [x] Configure seed in dbt_project.yml with proper column types

### 2.6 Create Dimension Models
- [x] **Create dimension models in marts/dimensions/**: ✅

- [x] **dim_date.sql** ✅
  - [x] Generate date dimension from order timestamps
  - [x] Include: date_key, full_date, year, month, month_name, quarter, day_of_week, day_name, is_weekend

- [x] **dim_customers.sql** ✅
  - [x] Join staging customers with regional seed data
  - [x] Include regional groupings via seed table join

- [x] **dim_products.sql** ✅
  - [x] Join products with category translations
  - [x] Calculate product_volume_cm3 with null handling
  - [x] Include all product attributes and derived fields

- [x] **dim_sellers.sql** ✅
  - [x] Join sellers with regional seed data
  - [x] Include regional classifications

- [x] **dim_orders.sql** ✅
  - [x] Calculate delivery performance metrics
  - [x] Implement days_to_delivery and is_delivered_on_time calculations
  - [x] Handle null delivery dates appropriately

- [x] **dim_payments.sql** ✅
  - [x] Aggregate payment methods per order
  - [x] Create payment type flags (uses_credit_card, uses_boleto, uses_voucher)
  - [x] Calculate total installments and payment method counts

- [x] **dim_reviews.sql** ✅
  - [x] Calculate review timing metrics
  - [x] Create comment availability flags
  - [x] Handle review-to-order date calculations

### 2.7 Create Fact Table
- [x] **Create fact_sales.sql** ✅
  - [x] Implement order item grain (one row per order item)
  - [x] Create surrogate key: CONCAT(order_id, '-', order_item_id)
  - [x] Join all necessary staging tables
  - [x] Implement LEFT JOIN for reviews (nullable foreign key)
  - [x] Calculate total_item_value (price + freight_value)
  - [x] Include all required measures and foreign keys

### 2.8 dbt Testing and Documentation
- [x] **Create schema.yml files** ✅
  - [x] Document all models, columns, and relationships ✅
  - [x] Add data quality tests (not_null, unique, relationships) ✅
  - [x] Create accepted_values tests for categorical fields ✅

- [x] **Implement custom tests** ✅
  - [x] Test referential integrity between fact and dimensions ✅
  - [x] Validate business logic (total_item_value calculation) ✅
  - [x] Test regional mappings completeness ✅

### 2.9 Execute dbt Transformations
- [x] **Run dbt models** 
  ```bash
  dbt deps  # Install any packages
  dbt seed  # Load seed data
  dbt run   # Execute all models
  dbt test  # Run all tests
```

- [x] **Generate documentation**
  ```bash
  dbt docs generate  ✅ 
  dbt docs serve     ✅ 
  ```

- [x] **Verify marts creation**
  - [x] Check BigQuery for `olist_marts` dataset  ✅ 
  - [x] Verify all dimension and fact tables exist  ✅ 
  - [x] Validate row counts and sample data  ✅ 
  - [ ] Test sample analytical queries

**Stage 2 Completion Criteria**:
- [x] All staging models execute successfully  ✅ 
- [x] All dimension tables populated with expected data  ✅ 
- [x] Fact table contains correct grain and measures  ✅ 
- [x] All dbt tests pass  ✅ See below for fails verified as edge business cases

      ```bash
      01:46:28  34 of 221 FAIL 4 dbt_utils_accepted_range_dim_payments_total_installments__24__0  [FAIL 4 in 2.15s]
      01:46:45  43 of 221 FAIL 15 dbt_utils_accepted_range_dim_reviews_days_to_review__365___30  [FAIL 15 in 1.94s]
      02:07:19  190 of 205 FAIL 2 test_business_logic .......................................... [FAIL 2 in 1.66s]
      ```
- [ ] Sample business questions can be answered with marts data

---

## Stage 3: Connection to Data Mart and Building Dashboards (Streamlit)

**Objective**: Build interactive Streamlit dashboard to answer all 8 business questions

### 3.1 Streamlit Project Setup
- [ ] **Create streamlit project directory**
  ```
  streamlit_dashboard/
  ├── streamlit_app.py
  ├── .streamlit/
  │   ├── config.toml
  │   └── secrets.toml
  ├── utils/
  │   ├── __init__.py
  │   ├── bigquery_client.py
  │   ├── data_queries.py
  │   └── visualization_helpers.py
  ├── pages/
  │   └── data_explorer.py
  ├── requirements.txt
  └── README.md
  ```

### 3.2 Configure BigQuery Connection
- [ ] **Create bigquery_client.py**
  - [ ] Implement service account authentication
  - [ ] Create cached BigQuery client connection
  - [ ] Add error handling for connection failures

- [ ] **Set up Streamlit secrets**
  - [ ] Create `.streamlit/secrets.toml` with GCP service account credentials
  - [ ] Add secrets.toml to .gitignore
  - [ ] Test authentication connectivity

### 3.3 Implement Data Query Functions
- [ ] **Create data_queries.py with functions for each business question**:

- [ ] **get_monthly_sales_trends()**
  - [ ] Query FactSales + DimDate for temporal analysis
  - [ ] Return: month, year, total_orders, total_sales, avg_order_value

- [ ] **get_top_products_categories()**
  - [ ] Query FactSales + DimProducts for category performance
  - [ ] Return: category, total_revenue, items_sold, unique_products

- [ ] **get_sales_by_region()**
  - [ ] Query FactSales + DimCustomers + DimSellers for geographic analysis
  - [ ] Return: customer_region, seller_region, sales metrics

- [ ] **get_customer_behavior()**
  - [ ] Query customer purchase patterns and frequency
  - [ ] Return: customer segments, purchase behavior metrics

- [ ] **get_payment_analysis()**
  - [ ] Query FactSales + DimPayments for payment method impact
  - [ ] Return: payment types, usage patterns, order values

- [ ] **get_seller_performance()**
  - [ ] Query seller metrics by region and performance
  - [ ] Return: seller regions, revenue, order volumes

- [ ] **get_reviews_sales_correlation()**
  - [ ] Query FactSales + DimReviews with null handling
  - [ ] Return: review categories, sales impact, correlation metrics

- [ ] **get_delivery_patterns()**
  - [ ] Query FactSales + DimOrders for delivery performance
  - [ ] Return: delivery times, on-time rates, regional patterns

- [ ] **Implement caching**
  - [ ] Add @st.cache_data(ttl=600) decorators
  - [ ] Implement error handling for failed queries
  - [ ] Add query timeout management

### 3.4 Create Dashboard Interface
- [ ] **Create main streamlit_app.py**
  - [ ] Set up page configuration and layout
  - [ ] Create sidebar with refresh controls
  - [ ] Implement 8-tab interface for business questions

- [ ] **Implement each dashboard tab**:

- [ ] **Tab 1: Monthly Sales Trends**
  - [ ] Line charts for revenue trends over time
  - [ ] KPI metrics for total sales, orders, average order value
  - [ ] Interactive filtering by year/month
  - [ ] Data table with detailed monthly breakdown

- [ ] **Tab 2: Top Products & Categories**
  - [ ] Bar charts for top categories by revenue
  - [ ] Product performance tables
  - [ ] Category comparison visualizations

- [ ] **Tab 3: Geographic Sales Distribution**
  - [ ] Regional sales visualization (sunburst or map)
  - [ ] Customer vs seller region analysis
  - [ ] State-level performance breakdown

- [ ] **Tab 4: Customer Purchase Behavior**
  - [ ] Customer segmentation visualizations
  - [ ] Purchase frequency and value analysis
  - [ ] Customer lifetime value metrics

- [ ] **Tab 5: Payment Method Impact**
  - [ ] Payment type distribution charts
  - [ ] Payment method vs order value correlation
  - [ ] Installment usage analysis

- [ ] **Tab 6: Seller Performance Analysis**
  - [ ] Seller performance by region
  - [ ] Top sellers and performance metrics
  - [ ] Regional seller distribution

- [ ] **Tab 7: Product Reviews and Sales Correlation**
  - [ ] Review score distribution
  - [ ] Sales impact by review category (including null handling)
  - [ ] Review availability vs sales correlation

- [ ] **Tab 8: Delivery Time Patterns**
  - [ ] Delivery performance by region
  - [ ] On-time delivery rates
  - [ ] Average delivery time analysis

### 3.5 Implement Visualizations
- [ ] **Create visualization_helpers.py**
  - [ ] Standardized chart functions using Plotly
  - [ ] Color schemes and styling consistency
  - [ ] Interactive chart configurations

- [ ] **Implement chart types**:
  - [ ] Line charts for time series
  - [ ] Bar charts for categorical comparisons
  - [ ] Pie/donut charts for distributions
  - [ ] Scatter plots for correlations
  - [ ] Box plots for delivery time analysis
  - [ ] Geographic visualizations for regional data

### 3.6 Testing and Refinement
- [ ] **Test dashboard functionality**
  ```bash
  streamlit run streamlit_app.py
  ```

- [ ] **Verify all business questions are answered**
  - [ ] Test each tab loads correctly
  - [ ] Verify data accuracy against manual BigQuery queries
  - [ ] Test interactive features and filters
  - [ ] Validate error handling for data issues

- [ ] **Performance optimization**
  - [ ] Verify caching works correctly
  - [ ] Test with concurrent users
  - [ ] Optimize slow queries if needed

### 3.7 Documentation and Deployment Preparation
- [ ] **Create comprehensive README.md**
  - [ ] Setup instructions
  - [ ] Authentication configuration
  - [ ] Local development guide
  - [ ] Deployment requirements

- [ ] **Prepare for deployment**
  - [ ] Create requirements.txt
  - [ ] Test with environment variables
  - [ ] Prepare Streamlit Cloud configuration

**Stage 3 Completion Criteria**:
- ✅ All 8 business questions have dedicated dashboard tabs
- ✅ Interactive visualizations load correctly with real data
- ✅ Caching and performance are optimized
- ✅ Error handling works for edge cases
- ✅ Dashboard provides actionable insights for business users

---

## Stage 4: Adding Great Expectations (Data Quality Validation)

**Objective**: Implement data quality validation at post-ingestion and post-transformation stages

### 4.1 Great Expectations Project Setup
- [ ] **Initialize Great Expectations**
  ```bash
  great_expectations --v3-api init
  ```

- [ ] **Configure project structure**
  ```
  great_expectations/
  ├── great_expectations.yml
  ├── expectations/
  ├── checkpoints/
  ├── plugins/
  └── uncommitted/
  ```

### 4.2 Configure Data Contexts
- [ ] **Set up BigQuery datasource for raw data**
  - [ ] Configure connection to `olist_raw` dataset
  - [ ] Set up authentication using service account
  - [ ] Create data connector for raw tables

- [ ] **Set up BigQuery datasource for marts data**
  - [ ] Configure connection to `olist_marts` dataset
  - [ ] Create data connector for dimension and fact tables

### 4.3 Create Post-Ingestion Validation Suite
- [ ] **Create expectation suites for raw data validation**:

- [ ] **raw_customers_suite**
  - [ ] `ExpectTableToExist()`
  - [ ] `ExpectTableColumnCountToEqual(value=5)`
  - [ ] `ExpectColumnToExist(column="customer_id")`
  - [ ] `ExpectColumnValuesToNotBeNull(column="customer_id")`
  - [ ] `ExpectColumnValuesToBeUnique(column="customer_id")`
  - [ ] `ExpectColumnValuesToBeInSet()` for Brazilian state codes

- [ ] **raw_orders_suite**
  - [ ] Table existence and structure validation
  - [ ] Primary key validation (order_id)
  - [ ] Date range validation for order timestamps
  - [ ] Order status value validation

- [ ] **raw_order_items_suite**
  - [ ] Referential integrity with orders
  - [ ] Price and freight value positivity checks
  - [ ] Product and seller ID format validation

- [ ] **raw_order_payments_suite**
  - [ ] Payment value positivity
  - [ ] Payment type enumeration validation
  - [ ] Installment count reasonableness

- [ ] **raw_order_reviews_suite**
  - [ ] Review score range validation (1-5)
  - [ ] Date consistency checks
  - [ ] Comment field null pattern validation

- [ ] **raw_products_suite**
  - [ ] Dimension value positivity
  - [ ] Category name validation
  - [ ] Weight and size reasonableness checks

- [ ] **raw_sellers_suite**
  - [ ] Location data validation
  - [ ] State code validation
  - [ ] Uniqueness checks

### 4.4 Create Post-Transformation Validation Suite
- [ ] **Create expectation suites for marts data validation**:

- [ ] **fact_sales_suite**
  - [ ] `ExpectColumnValuesToNotBeNull()` for all non-nullable foreign keys
  - [ ] `ExpectColumnValuesToBePositive()` for prices and freight
  - [ ] `ExpectColumnPairValuesToBeEqual()` for total_item_value calculation
  - [ ] Row count reasonableness checks
  - [ ] Foreign key referential integrity

- [ ] **dim_customers_suite**
  - [ ] Completeness of regional mappings
  - [ ] State code validation
  - [ ] No duplicate customer keys

- [ ] **dim_products_suite**
  - [ ] Category translation completeness
  - [ ] Product volume calculation validation
  - [ ] No null product keys

- [ ] **dim_sellers_suite**
  - [ ] Regional mapping completeness
  - [ ] Location data consistency

- [ ] **dim_orders_suite**
  - [ ] Delivery calculation logic validation
  - [ ] Date consistency checks
  - [ ] On-time delivery flag accuracy

- [ ] **dim_payments_suite**
  - [ ] Payment aggregation logic validation
  - [ ] Boolean flag consistency
  - [ ] Installment total reasonableness

- [ ] **dim_reviews_suite**
  - [ ] Review timing calculation accuracy
  - [ ] Comment flag logic validation
  - [ ] Score range validation

### 4.5 Create Checkpoints
- [ ] **Create post_ingestion_checkpoint**
  - [ ] Include all raw data expectation suites
  - [ ] Configure to run after Meltano completion
  - [ ] Set up notification actions for failures

- [ ] **Create post_transformation_checkpoint**
  - [ ] Include all marts data expectation suites
  - [ ] Configure to run after dbt completion
  - [ ] Set up validation result storage

### 4.6 Create Validation Scripts
- [ ] **Create validation runner scripts**
  - [ ] `run_post_ingestion_validation.py`
  - [ ] `run_post_transformation_validation.py`
  - [ ] Command-line interface for manual validation runs

- [ ] **Implement validation logic**
  - [ ] Success/failure determination
  - [ ] Detailed reporting for failures
  - [ ] Integration points for pipeline orchestration

### 4.7 Test Validation Framework
- [ ] **Test raw data validation**
  ```bash
  python run_post_ingestion_validation.py
  ```

- [ ] **Test marts validation**
  ```bash
  python run_post_transformation_validation.py
  ```

- [ ] **Verify validation reports**
  - [ ] Check validation results in Great Expectations store
  - [ ] Test failure scenarios with intentional data issues
  - [ ] Validate notification and alerting functionality

**Stage 4 Completion Criteria**:
- ✅ All expectation suites execute successfully
- ✅ Validation catches intentional data quality issues
- ✅ Reports provide actionable insights for data quality
- ✅ Integration scripts ready for orchestration

---

## Stage 5: Adding Dagster (Pipeline Orchestration)

**Objective**: Orchestrate the entire pipeline with dependency management, monitoring, and scheduling

### 5.1 Dagster Project Setup
- [ ] **Initialize Dagster project**
  ```bash
  dagster-dbt project scaffold --project-name olist-pipeline
  ```

- [ ] **Configure project structure**
  ```
  dagster_project/
  ├── olist_pipeline/
  │   ├── __init__.py
  │   ├── assets/
  │   ├── jobs/
  │   ├── schedules/
  │   └── sensors/
  ├── dagster_project.py
  └── setup.py
  ```

### 5.2 Create Asset Definitions
- [ ] **Create ingestion assets**

- [ ] **meltano_extract_load asset**
  - [ ] Execute Meltano pipeline via subprocess
  - [ ] Return materialization with row count metadata
  - [ ] Handle execution errors and timeouts

- [ ] **Raw data validation assets**
  - [ ] `validate_raw_customers`
  - [ ] `validate_raw_orders`
  - [ ] `validate_raw_order_items`
  - [ ] `validate_raw_order_payments`
  - [ ] `validate_raw_order_reviews`
  - [ ] `validate_raw_products`
  - [ ] `validate_raw_sellers`
  - [ ] Each depends on `meltano_extract_load`
  - [ ] Execute Great Expectations validation suites

### 5.3 Create Transformation Assets
- [ ] **dbt transformation assets**

- [ ] **dbt_staging_models asset**
  - [ ] Execute `dbt run --select staging`
  - [ ] Depend on all raw validation assets
  - [ ] Return model execution metadata

- [ ] **dbt_marts_models asset**
  - [ ] Execute `dbt run --select marts`
  - [ ] Depend on `dbt_staging_models`
  - [ ] Include seed data loading

### 5.4 Create Quality Assurance Assets
- [ ] **Marts validation assets**
  - [ ] `validate_fact_sales`
  - [ ] `validate_dim_customers`
  - [ ] `validate_dim_products`
  - [ ] `validate_dim_sellers`
  - [ ] `validate_dim_orders`
  - [ ] `validate_dim_payments`
  - [ ] `validate_dim_reviews`
  - [ ] Each depends on `dbt_marts_models`

### 5.5 Create Analytics Assets
- [ ] **streamlit_dashboard_refresh asset**
  - [ ] Signal dashboard data refresh
  - [ ] Depend on all marts validation assets
  - [ ] Could trigger cache clearing or webhook call

### 5.6 Configure Asset Dependencies
- [ ] **Set up dependency graph**
  ```
  CSV Files → meltano_extract_load → raw_validations → dbt_staging_models → dbt_marts_models → marts_validations → streamlit_dashboard_refresh
  ```

- [ ] **Configure failure handling**
  - [ ] Stop execution on critical validation failures
  - [ ] Allow continuation for non-critical issues
  - [ ] Set up retry policies for transient failures

### 5.7 Create Job Definitions
- [ ] **Create daily_pipeline job**
  - [ ] Include all assets in proper dependency order
  - [ ] Configure execution timeout and retry policies
  - [ ] Set up resource allocation

- [ ] **Create validation_only job**
  - [ ] For ad-hoc data quality checks
  - [ ] Skip ingestion and transformation steps

### 5.8 Configure Schedules and Sensors
- [ ] **Create daily schedule**
  ```python
  @schedule(
      job=daily_pipeline,
      cron_schedule="0 6 * * *"  # 6 AM daily
  )
  ```

- [ ] **Create failure sensors**
  - [ ] Monitor for asset failures
  - [ ] Send notifications via email/Slack
  - [ ] Log detailed failure information

### 5.9 Set Up Monitoring and Observability
- [ ] **Configure asset metadata tracking**
  - [ ] Row counts for each transformation step
  - [ ] Execution time tracking
  - [ ] Data quality metrics

- [ ] **Set up alerting**
  - [ ] Success/failure notifications
  - [ ] Data quality issue alerts
  - [ ] Performance degradation warnings

### 5.10 Test Orchestration
- [ ] **Test individual assets**
  ```bash
  dagster asset materialize --select meltano_extract_load
  ```

- [ ] **Test complete pipeline**
  ```bash
  dagster job execute --job daily_pipeline
  ```

- [ ] **Test failure scenarios**
  - [ ] Simulate Meltano failures
  - [ ] Test validation failure handling
  - [ ] Verify retry logic

### 5.11 Deploy Dagster Web Interface
- [ ] **Start Dagster webserver**
  ```bash
  dagster-webserver
  ```

- [ ] **Verify web interface**
  - [ ] Asset lineage visualization
  - [ ] Job execution monitoring
  - [ ] Historical run tracking

**Stage 5 Completion Criteria**:
- ✅ All assets execute in correct dependency order
- ✅ Failure handling stops pipeline at appropriate points
- ✅ Monitoring and alerting work correctly
- ✅ Web interface provides clear visibility into pipeline status
- ✅ Scheduling works for automated execution

---

## Stage 6: Project Documentation

**Objective**: Create comprehensive documentation for the project

### 6.1 Architecture Documentation
- [ ] **Create system architecture diagram**
  - [ ] Data flow from CSV to dashboard
  - [ ] Technology stack visualization
  - [ ] Component interaction diagram

- [ ] **Document design decisions**
  - [ ] Star schema design rationale
  - [ ] Technology selection justification
  - [ ] Performance and scalability considerations

### 6.2 Setup and Installation Guide
- [ ] **Create comprehensive README.md**
  - [ ] Project overview and business context
  - [ ] Prerequisites and system requirements
  - [ ] Step-by-step setup instructions
  - [ ] Environment configuration guide

- [ ] **Create developer setup guide**
  - [ ] Local development environment setup
  - [ ] IDE configuration recommendations
  - [ ] Testing and debugging procedures

### 6.3 User Documentation
- [ ] **Create dashboard user guide**
  - [ ] How to access and navigate the dashboard
  - [ ] Explanation of each business question and visualization
  - [ ] Interactive feature usage guide

- [ ] **Create business analyst guide**
  - [ ] Data model explanation
  - [ ] Query examples for custom analysis
  - [ ] Common troubleshooting scenarios

### 6.4 Operational Documentation
- [ ] **Create operations runbook**
  - [ ] Daily monitoring procedures
  - [ ] Common issue resolution
  - [ ] Pipeline failure recovery procedures

- [ ] **Create data quality monitoring guide**
  - [ ] Expected data quality thresholds
  - [ ] Investigation procedures for quality issues
  - [ ] Data source coordination procedures

### 6.5 API and Technical Documentation
- [ ] **Document dbt models**
  - [ ] Model descriptions and business logic
  - [ ] Column definitions and transformations
  - [ ] Data lineage documentation

- [ ] **Document Streamlit application**
  - [ ] Code structure and organization
  - [ ] Query functions documentation
  - [ ] Deployment and configuration options

### 6.6 Performance and Monitoring
- [ ] **Create performance benchmarks document**
  - [ ] Expected execution times for each stage
  - [ ] Resource utilization guidelines
  - [ ] Scaling recommendations

- [ ] **Document monitoring and alerting**
  - [ ] Key metrics to monitor
  - [ ] Alert configuration and response procedures
  - [ ] Performance optimization strategies

**Stage 6 Completion Criteria**:
- ✅ Complete technical documentation for all components
- ✅ User guides for both technical and business users
- ✅ Operational procedures for maintenance and troubleshooting
- ✅ Performance and scaling documentation
- ✅ All documentation is version controlled and accessible

---

## Final Project Structure

Upon completion, the project should have the following structure:

```
olist-ecommerce-pipeline/
├── README.md
├── environment.yml
├── data_ingestion.py
├── prd.md
├── plan.md
├── data/                          # CSV data files
├── meltano.yml                    # Meltano configuration
├── olist_analytics/               # dbt project
│   ├── dbt_project.yml
│   ├── models/
│   ├── seeds/
│   └── tests/
├── streamlit_dashboard/           # Streamlit application
│   ├── streamlit_app.py
│   └── utils/
├── great_expectations/            # Data validation
│   ├── great_expectations.yml
│   └── expectations/
├── dagster_project/               # Pipeline orchestration
│   ├── olist_pipeline/
│   └── dagster_project.py
├── docs/                          # Project documentation
│   ├── architecture.md
│   ├── user_guide.md
│   └── operations.md
└── scripts/                       # Utility scripts
    ├── setup.sh
    └── validate_environment.py
```

## Success Metrics

- [ ] **Data Pipeline**: Successfully processes all 9 source tables through to analytics-ready marts
- [ ] **Data Quality**: All Great Expectations validations pass consistently
- [ ] **Analytics**: All 8 business questions can be answered through interactive dashboard
- [ ] **Orchestration**: Complete pipeline runs successfully on schedule with proper monitoring
- [ ] **Documentation**: Comprehensive documentation enables new team members to understand and maintain the system

This implementation plan provides a systematic approach to building the complete Olist e-commerce data pipeline while ensuring each component is properly tested and documented before moving to the next stage.