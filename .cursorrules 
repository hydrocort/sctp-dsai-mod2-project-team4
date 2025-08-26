# CLAUDE.md

This file provides guidance to Claude Code when working with this Olist E-commerce Data Pipeline project.

## Project Overview

**Purpose**: End-to-end data pipeline for Brazilian e-commerce analytics
**Tech Stack**: Python, Meltano, BigQuery, dbt, Great Expectations, Dagster, Streamlit
**Goal**: Transform raw CSV data into interactive dashboards answering 8 business questions

## Core Principles

### KISS (Keep It Simple, Stupid)
- Solutions must be straightforward and easy to understand
- Avoid over-engineering or unnecessary abstraction
- Prioritize code readability and maintainability

### YAGNI (You Aren't Gonna Need It)
- Do not add speculative features or future-proofing unless explicitly required
- Focus only on immediate requirements and deliverables
- Minimize code bloat and long-term technical debt

## Key Project Files

- `prd.md` - Complete project requirements and specifications
- `plan.md` - Step-by-step implementation plan with stages
- `environment.yml` - Conda environment with all required dependencies
- `data_ingestion.py` - Already completed data download script

## Architecture Context

**Data Flow**: CSV → Meltano → BigQuery Raw → Great Expectations → dbt → BigQuery Marts → Great Expectations → Streamlit

**Key Decisions Made**:
- Single mart approach (`olist_marts` dataset)
- Null handling for reviews (LEFT JOIN, no surrogate keys)
- Historical dataset (no SCD Type 2 or snapshots)
- Complete Brazilian state seed file for regional groupings
- Order item grain for fact table (one row per order item)

## Technology-Specific Guidelines

### Meltano
- Use `tap-csv` for extraction, `target-bigquery` for loading
- Configure table naming with `raw_` prefix
- Store service account key securely, add to .gitignore

### dbt
- Staging models as views, marts as tables
- Use `{{ ref() }}` and `{{ source() }}` functions
- Implement proper testing with schema.yml
- Follow naming convention: `stg_*` for staging, `dim_*` for dimensions, `fact_*` for facts

### BigQuery
- Three datasets: `olist_raw`, `olist_staging`, `olist_marts`
- Use proper data types (not all STRING)
- Optimize for analytical queries

### Great Expectations
- Post-ingestion validation for raw data quality
- Post-transformation validation for business logic
- Focus on critical validations, avoid over-testing

### Dagster
- Define assets with clear dependencies
- Implement proper error handling and retries
- Use descriptive asset names and metadata

### Streamlit
- Use service account authentication via secrets.toml
- Implement caching with `@st.cache_data(ttl=600)`
- Create 8 tabs for business questions
- Handle BigQuery connection errors gracefully

## Coding Standards

### General Python
- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings for functions and classes
- Handle exceptions appropriately
- Use type hints where beneficial

### SQL (dbt)
- Use consistent indentation (2 spaces)
- Write readable, well-commented SQL
- Use CTEs for complex queries
- Avoid SELECT * in production models

### Configuration Files
- Use YAML for configuration (dbt, Meltano, Great Expectations)
- Include comments explaining non-obvious settings
- Version control all configuration files
- Use environment variables for secrets

## Data Quality Standards

- All primary keys must be unique and not null
- Foreign keys must reference valid dimension records
- Monetary values must be positive
- Brazilian state codes must be valid (AC, AL, AM, etc.)
- Dates must be reasonable for e-commerce context

## File Organization

```
project/
├── meltano.yml                 # Meltano configuration
├── olist_analytics/            # dbt project
│   ├── models/staging/
│   ├── models/marts/dimensions/
│   ├── models/marts/facts/
│   └── seeds/
├── streamlit_dashboard/        # Streamlit app
├── great_expectations/         # Data validation
└── dagster_project/           # Orchestration
```

## Common Patterns

### Error Handling
```python
try:
    result = operation()
    return result
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### BigQuery Connections
```python
@st.cache_resource
def init_connection():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return bigquery.Client(credentials=credentials)
```

### dbt Model Structure
```sql
{{ config(materialized='table') }}

WITH source_data AS (
    SELECT * FROM {{ ref('stg_table') }}
),

final AS (
    SELECT 
        key,
        calculated_field,
        derived_metric
    FROM source_data
    WHERE condition
)

SELECT * FROM final
```

## Business Context

**8 Core Business Questions**:
1. Monthly sales trends
2. Top products/categories  
3. Geographic sales distribution
4. Customer purchase behavior
5. Payment method impact
6. Seller performance analysis
7. Product reviews correlation
8. Delivery time patterns

**Data Sources**: 9 CSV files from Brazilian e-commerce (customers, orders, products, etc.)

## Development Workflow

1. **Always reference prd.md and plan.md** for requirements and current stage
2. **Test incrementally** - verify each stage before proceeding
3. **Document changes** - update relevant files when making modifications  
4. **Follow the implementation sequence** from plan.md
5. **Validate data quality** at each transformation step

## Important Notes

- Project uses `mod2proj` conda environment
- Data is historical (no need for real-time considerations)
- Focus on analytical performance over transactional integrity
- Brazilian context (states, regions, Portuguese product categories)
- Review field can be NULL (intentional design decision)

When working on this project, always consider the end goal: creating reliable, maintainable analytics pipeline that answers business questions through interactive dashboards.