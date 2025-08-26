# Olist E-commerce Data Pipeline Project

A comprehensive data engineering and analytics project that processes Brazilian e-commerce data using modern data stack tools including Meltano, dbt, and BigQuery.

## 🎯 Project Overview

This project implements a complete data pipeline that:

[To be filled in later]

## 🏗️ Architecture

```
[To be filled in later]
```

## 🚀 Quick Start (New Machine Setup)

### Prerequisites
- **Conda/Miniconda** installed
- **Python 3.11** 
- **Google Cloud Platform** account with BigQuery access
- **Git** for cloning the repository
- **Kaggle account** with API access (for downloading datasets)

### Step 1: Clone and Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd sctp-dsai-mod2-project-team4

# Create and activate conda environment
conda env create -f environment.yml
conda activate mod2proj
```

### Step 2: Setup Credentials
```bash
# Create credentials directory at project root
mkdir credentials

# Copy environment template
cp .env.template .env

# Add your GCP service account key to credentials/ directory
# Download your service account JSON key from Google Cloud Console
# Place it in the credentials/ folder you just created
# Ensure the file path in .env matches your actual filename
```

**Required Environment Variables:**
```bash
GOOGLE_APPLICATION_CREDENTIALS=credentials/your-service-account-key.json
GCP_PROJECT_ID=your-project-id
BQ_LOCATION=US
DATA_PATH=./data/brazilian-ecommerce/
```

### Step 3: Setup Kaggle API Credentials
```bash
# Download your Kaggle API credentials
# Go to: https://www.kaggle.com/settings -> API -> Create New API Token
# This will download a kaggle.json file

# Place kaggle.json in the project root directory
# The script will automatically configure it for you
```

**Note:** The `kaggle.json` file contains your API username and key. Keep it secure and don't commit it to git.

### Step 4: Download CSV Files from Kaggle
```bash
# Download CSV datasets from Kaggle
python data_ingestion.py
```

**Note:** This downloads CSV files to the `data/` directory. Skip if you already have the data files.

### Step 5: Generate Local Data
```bash
# Create local DuckDB database for analysis
python load_csv_to_duckdb.py
```

**Note:** This creates `olist_data.duckdb` (~58MB) locally. Skip if you only need BigQuery data.

### Step 6: Setup Meltano
```bash
# Install Meltano plugins (creates .meltano/ directory)
meltano install
```

**What this does:**
- Installs `tap-duckdb` extractor
- Installs `target-bigquery` loader
- Sets up plugin configurations

### Step 7: Load Data to BigQuery (Optional)
```bash
# Only run if not already done
meltano invoke tap-duckdb target-bigquery
```

**Skip this step if:**
- Data is already in BigQuery
- You're just setting up a development environment
- You're using existing production data

### Step 8: Setup dbt
```bash
# Navigate to dbt project
cd olist_analytics

# Install dependencies
dbt deps

# Build models (only if not already done)
dbt build
```

**Skip `dbt build` if:**
- Models are already built in BigQuery
- You're just setting up the environment
- Data hasn't changed

## 📁 Project Structure

```
├── data/                          # Raw CSV data (not committed)
├── olist_analytics/              # dbt project
│   ├── models/                   # Data transformation models
│   ├── profiles.yml             # BigQuery connection config
│   └── dbt_project.yml          # dbt project config
├── plugins/                      # Meltano plugin definitions
├── credentials/                  # GCP service account keys (not committed)
├── meltano.yml                   # Meltano pipeline configuration
├── environment.yml               # Conda environment dependencies
├── setup_environment.sh          # Environment setup script
└── load_csv_to_duckdb.py        # Data ingestion script
```

## 🔧 Configuration Files

### meltano.yml
- **Extractors**: `tap-duckdb` for DuckDB data extraction
- **Loaders**: `target-bigquery` for BigQuery data loading
- **Pipeline**: Complete ELT configuration

### olist_analytics/profiles.yml
- **BigQuery Connection**: Uses environment variables for security
- **Multiple Environments**: dev/prod configurations
- **No Hardcoded Credentials**: Safe to commit

### environment.yml
- **Python 3.11**: Core Python version
- **Data Tools**: pandas, numpy, matplotlib, seaborn
- **Pipeline Tools**: Meltano, dbt, DuckDB
- **Cloud Tools**: Google Cloud libraries
- **Web Tools**: Streamlit for dashboards

## 🚫 What's NOT Committed

The following items are intentionally excluded from git:
- **Database files**: `*.duckdb`, `*.db` (regenerated locally)
- **Credentials**: `credentials/` directory (add your own)
- **Environment files**: `.env` (copy from `.env.template`)
- **Runtime state**: `.meltano/` directory (created by `meltano install`)
- **Build artifacts**: `olist_analytics/target/` (created by `dbt build`)
- **Log files**: `logs/` directory (generated during execution)
- **Raw data**: `data/` directory (download from Kaggle)

## 📊 Data Sources

- **Brazilian E-commerce**: Customer orders, products, reviews
- **Marketing Funnel**: Customer acquisition and conversion data
- **Source**: Kaggle datasets (automatically downloaded)

## 🔄 Data Pipeline

1. **Extract**: CSV files → DuckDB (local processing)
2. **Load**: DuckDB → BigQuery (cloud storage)
3. **Transform**: BigQuery → dbt models (business logic)
4. **Serve**: Analytics marts (business intelligence)

## 🧪 Testing Your Setup

```bash
# Test Meltano
meltano --version
meltano invoke --help

# Test dbt
cd olist_analytics
dbt --version
dbt debug

# Test BigQuery connection
dbt debug --config-dir
```

## 🆘 Troubleshooting

### Common Issues:

**"Credentials not found"**
- Ensure `GOOGLE_APPLICATION_CREDENTIALS` is set
- Check that service account key exists in `credentials/`

**"BigQuery dataset not found"**
- Create dataset manually in BigQuery console
- Or run `meltano invoke tap-duckdb target-bigquery` first

**"dbt profile not found"**
- Ensure you're in the `olist_analytics/` directory
- Check that `profiles.yml` exists and is properly formatted

**"Meltano plugins not found"**
- Run `meltano install` to install plugins
- Check `meltano.yml` for correct plugin configurations

## 📚 Additional Resources

- **Meltano Documentation**: https://docs.meltano.com/
- **dbt Documentation**: https://docs.getdbt.com/
- **BigQuery Documentation**: https://cloud.google.com/bigquery/docs
- **Project Plan**: See `plan.md` for detailed implementation steps

## 🤝 Contributing

1. Follow the existing code structure
2. Update documentation for any new features
3. Test your changes on a fresh environment
4. Ensure all sensitive data is properly excluded

## 📄 License

This project is part of the SCTP Data Science & AI Module 2 curriculum.

---

**Happy Data Engineering! 🚀**
