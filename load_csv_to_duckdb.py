#!/usr/bin/env python3
"""
Stage 1A: Load CSV files directly into DuckDB
Hybrid Data Pipeline: CSV → DuckDB → BigQuery (via Meltano)

This script loads all 9 Olist Brazilian e-commerce CSV files into DuckDB tables
for reliable data handling before transferring to BigQuery via Meltano.
"""

import os
import sys
import duckdb
from pathlib import Path
import logging
from typing import Dict, List, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data" / "brazilian-ecommerce"
DUCKDB_PATH = PROJECT_ROOT / "olist_data.duckdb"

# CSV file mappings: (csv_filename, table_name, description)
CSV_TABLES = [
    ("olist_customers_dataset.csv", "raw_customers", "Customer information"),
    ("olist_orders_dataset.csv", "raw_orders", "Order information"), 
    ("olist_order_items_dataset.csv", "raw_order_items", "Order line items"),
    ("olist_order_payments_dataset.csv", "raw_order_payments", "Payment information"),
    ("olist_order_reviews_dataset.csv", "raw_order_reviews", "Customer reviews"),
    ("olist_products_dataset.csv", "raw_products", "Product catalog"),
    ("olist_sellers_dataset.csv", "raw_sellers", "Seller information"),
    ("olist_geolocation_dataset.csv", "raw_geolocation", "Geographic coordinates"),
    ("product_category_name_translation.csv", "raw_category_translation", "Category translations")
]

def check_csv_files() -> bool:
    """Verify all required CSV files exist."""
    logger.info("🔍 Checking CSV files...")
    
    missing_files = []
    for csv_file, _, _ in CSV_TABLES:
        csv_path = DATA_DIR / csv_file
        if not csv_path.exists():
            missing_files.append(csv_file)
        else:
            file_size = csv_path.stat().st_size / (1024 * 1024)  # MB
            logger.info(f"  ✅ {csv_file} ({file_size:.1f} MB)")
    
    if missing_files:
        logger.error(f"❌ Missing CSV files: {missing_files}")
        return False
    
    logger.info("✅ All CSV files found!")
    return True

def get_csv_row_count(csv_path: Path) -> int:
    """Get row count from CSV file (excluding header)."""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Count lines and subtract 1 for header
            return sum(1 for _ in f) - 1
    except Exception as e:
        logger.warning(f"Could not count rows in {csv_path}: {e}")
        return -1

def create_duckdb_database() -> duckdb.DuckDBPyConnection:
    """Create or connect to DuckDB database."""
    logger.info(f"🦆 Creating DuckDB database: {DUCKDB_PATH}")
    
    # Remove existing database to start fresh
    if DUCKDB_PATH.exists():
        DUCKDB_PATH.unlink()
        logger.info("  📝 Removed existing database")
    
    # Create new connection
    conn = duckdb.connect(str(DUCKDB_PATH))
    logger.info("✅ DuckDB database created successfully!")
    
    return conn

def load_csv_to_table(conn: duckdb.DuckDBPyConnection, csv_file: str, table_name: str, description: str) -> Tuple[bool, int]:
    """Load a single CSV file into DuckDB table."""
    csv_path = DATA_DIR / csv_file
    
    logger.info(f"📊 Loading {csv_file} → {table_name}")
    logger.info(f"    Description: {description}")
    
    try:
        # Get original CSV row count
        original_rows = get_csv_row_count(csv_path)
        logger.info(f"    Original CSV rows: {original_rows:,}")
        
        # Use DuckDB's read_csv_auto for automatic schema detection
        create_table_sql = f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path}', header=true)
        """
        
        conn.execute(create_table_sql)
        
        # Verify table creation and get row count
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        loaded_rows = result[0] if result else 0
        
        # Get column count
        columns_result = conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
        column_count = len(columns_result)
        
        logger.info(f"    ✅ Loaded: {loaded_rows:,} rows, {column_count} columns")
        
        # Validate row count matches
        if original_rows > 0 and loaded_rows != original_rows:
            logger.warning(f"    ⚠️  Row count mismatch! CSV: {original_rows:,}, DuckDB: {loaded_rows:,}")
        
        return True, loaded_rows
        
    except Exception as e:
        logger.error(f"    ❌ Failed to load {csv_file}: {e}")
        return False, 0

def validate_database(conn: duckdb.DuckDBPyConnection) -> Dict[str, int]:
    """Validate the created database and return table statistics."""
    logger.info("🔍 Validating DuckDB database...")
    
    table_stats = {}
    
    try:
        # Get list of tables
        tables_result = conn.execute("SHOW TABLES").fetchall()
        table_names = [row[0] for row in tables_result]
        
        logger.info(f"  📋 Found {len(table_names)} tables:")
        
        for table_name in table_names:
            # Get row count
            row_count_result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
            row_count = row_count_result[0] if row_count_result else 0
            
            # Get column info
            columns_result = conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
            column_count = len(columns_result)
            
            table_stats[table_name] = row_count
            logger.info(f"    📊 {table_name}: {row_count:,} rows, {column_count} columns")
        
        # Test a sample query
        logger.info("  🧪 Testing sample queries...")
        sample_query = "SELECT COUNT(*) as total_customers FROM raw_customers"
        result = conn.execute(sample_query).fetchone()
        logger.info(f"    ✅ Sample query successful: {result[0]:,} customers")
        
        return table_stats
        
    except Exception as e:
        logger.error(f"  ❌ Database validation failed: {e}")
        return {}

def main():
    """Main execution function."""
    logger.info("🚀 Starting CSV to DuckDB loading process...")
    
    # Check prerequisites
    if not check_csv_files():
        sys.exit(1)
    
    # Create DuckDB database
    conn = create_duckdb_database()
    
    try:
        # Load all CSV files
        total_rows = 0
        successful_loads = 0
        
        for csv_file, table_name, description in CSV_TABLES:
            success, rows = load_csv_to_table(conn, csv_file, table_name, description)
            if success:
                successful_loads += 1
                total_rows += rows
            else:
                logger.error(f"Failed to load {csv_file}")
        
        # Summary
        logger.info("📈 Loading Summary:")
        logger.info(f"  ✅ Successfully loaded: {successful_loads}/{len(CSV_TABLES)} tables")
        logger.info(f"  📊 Total rows loaded: {total_rows:,}")
        
        if successful_loads == len(CSV_TABLES):
            # Validate database
            table_stats = validate_database(conn)
            
            if table_stats:
                logger.info("🎉 Stage 1A Complete!")
                logger.info(f"  📁 DuckDB database: {DUCKDB_PATH}")
                logger.info(f"  📊 Total tables: {len(table_stats)}")
                logger.info(f"  🔢 Total records: {sum(table_stats.values()):,}")
                logger.info("  ✅ Ready for Stage 1B: DuckDB → BigQuery via Meltano")
            else:
                logger.error("❌ Database validation failed")
                sys.exit(1)
        else:
            logger.error("❌ Not all tables loaded successfully")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Critical error during loading: {e}")
        sys.exit(1)
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()


