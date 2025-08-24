#!/usr/bin/env python3
"""
Data Ingestion Script for Olist E-Commerce and Marketing Funnel Datasets

This script downloads and organizes the Olist datasets from Kaggle into a structured 
data directory at the project root. It handles both the Brazilian E-Commerce dataset 
and the Marketing Funnel dataset.

Requirements:
- kaggle.json file in the project root for API authentication
- kaggle package installed (pip install kaggle)

Usage:
    python data_ingestion.py

The script will:
1. Set up Kaggle API authentication
2. Create necessary folder structure
3. Download datasets if not already present
4. Extract and organize files
5. Verify all expected files are present
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os
import zipfile
import shutil
import json
import sys
import warnings
warnings.filterwarnings('ignore')


def setup_kaggle_datasets():
    """
    Download and setup Olist datasets from Kaggle using API
    This function will:
    1. Check if kaggle.json exists and set up authentication
    2. Create necessary folder structure
    3. Download datasets if not already present
    4. Extract and organize files
    
    Returns:
        bool: True if setup successful, False otherwise
    """
    
    print("=== KAGGLE DATASET SETUP ===")
    print("Setting up Olist E-commerce and Marketing Funnel datasets...")
    print("-" * 60)
    
    # Check if kaggle.json exists in project root
    kaggle_json_path = Path('./kaggle.json')
    if not kaggle_json_path.exists():
        print("❌ Error: kaggle.json file not found in project root!")
        print("Please ensure your Kaggle API credentials are in kaggle.json")
        print("You can download it from: https://www.kaggle.com/settings -> API -> Create New API Token")
        return False
    
    # Set up Kaggle authentication
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    
    # Copy kaggle.json to ~/.kaggle/ if not already there
    target_kaggle_json = kaggle_dir / 'kaggle.json'
    if not target_kaggle_json.exists():
        shutil.copy2(kaggle_json_path, target_kaggle_json)
        # Set proper permissions (required by Kaggle API)
        os.chmod(target_kaggle_json, 0o600)
        print("✓ Kaggle credentials configured")
    
    # Create data directory structure
    data_dir = Path('./data')
    ecommerce_dir = data_dir / 'brazilian-ecommerce'
    marketing_dir = data_dir / 'marketing-funnel'
    
    # Create directories
    ecommerce_dir.mkdir(parents=True, exist_ok=True)
    marketing_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created directory structure: {data_dir}")
    
    # Import kaggle after setting up credentials
    try:
        import kaggle
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        print("✓ Kaggle API authenticated successfully")
    except ImportError:
        print("❌ Error: kaggle package not installed!")
        print("Install with: pip install kaggle")
        return False
    except Exception as e:
        print(f"❌ Error authenticating with Kaggle API: {e}")
        return False
    
    # Dataset configurations
    datasets = {
        'brazilian-ecommerce': {
            'dataset': 'olistbr/brazilian-ecommerce',
            'target_dir': ecommerce_dir,
            'expected_files': [
                'olist_customers_dataset.csv',
                'olist_orders_dataset.csv',
                'olist_order_items_dataset.csv',
                'olist_order_payments_dataset.csv',
                'olist_order_reviews_dataset.csv',
                'olist_products_dataset.csv',
                'olist_sellers_dataset.csv',
                'olist_geolocation_dataset.csv',
                'product_category_name_translation.csv'
            ]
        },
        'marketing-funnel': {
            'dataset': 'olistbr/marketing-funnel-olist',
            'target_dir': marketing_dir,
            'expected_files': [
                'olist_marketing_qualified_leads_dataset.csv',
                'olist_closed_deals_dataset.csv'
            ]
        }
    }
    
    # Download and extract datasets
    for dataset_name, config in datasets.items():
        print(f"\n--- Processing {dataset_name} ---")
        
        # Check if files already exist
        existing_files = [f for f in config['expected_files'] 
                         if (config['target_dir'] / f).exists()]
        
        if len(existing_files) == len(config['expected_files']):
            print(f"✓ All files already exist for {dataset_name}")
            # Show file sizes for verification
            for file in config['expected_files']:
                file_path = config['target_dir'] / file
                if file_path.exists():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"  - {file}: {size_mb:.1f} MB")
            continue
        
        print(f"📥 Downloading {dataset_name} dataset...")
        try:
            # Download dataset
            api.dataset_download_files(
                config['dataset'], 
                path=config['target_dir'], 
                unzip=True,
                quiet=False
            )
            print(f"✓ Downloaded and extracted {dataset_name}")
            
            # Verify files
            missing_files = [f for f in config['expected_files'] 
                           if not (config['target_dir'] / f).exists()]
            
            if missing_files:
                print(f"⚠️  Warning: Some expected files are missing from {dataset_name}:")
                for file in missing_files:
                    print(f"  - {file}")
            else:
                print(f"✓ All expected files present for {dataset_name}")
                # Show file sizes
                for file in config['expected_files']:
                    file_path = config['target_dir'] / file
                    if file_path.exists():
                        size_mb = file_path.stat().st_size / (1024 * 1024)
                        print(f"  - {file}: {size_mb:.1f} MB")
            
        except Exception as e:
            print(f"❌ Error downloading {dataset_name}: {e}")
            return False
    
    # Clean up any zip files that might be left
    for zip_file in data_dir.rglob("*.zip"):
        try:
            zip_file.unlink()
            print(f"🗑️  Cleaned up {zip_file.name}")
        except:
            pass
    
    print("\n" + "="*60)
    print("✅ DATASET SETUP COMPLETE!")
    print("All datasets are ready for analysis.")
    print("="*60)
    
    return True


def load_datasets():
    """
    Load all datasets into memory and return dictionaries containing the DataFrames
    
    Returns:
        tuple: (ecommerce_data, marketing_data) - dictionaries with loaded DataFrames
    """
    
    print("\n=== LOADING DATASETS ===")
    print("Loading all datasets into memory...")
    print("-" * 40)
    
    # Define file paths
    ecommerce_path = Path('./data/brazilian-ecommerce/')
    marketing_path = Path('./data/marketing-funnel/')
    
    # E-Commerce dataset files
    ecommerce_files = {
        'customers': 'olist_customers_dataset.csv',
        'orders': 'olist_orders_dataset.csv', 
        'order_items': 'olist_order_items_dataset.csv',
        'order_payments': 'olist_order_payments_dataset.csv',
        'order_reviews': 'olist_order_reviews_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'sellers': 'olist_sellers_dataset.csv',
        'geolocation': 'olist_geolocation_dataset.csv',
        'category_translation': 'product_category_name_translation.csv'
    }
    
    # Marketing Funnel dataset files
    marketing_files = {
        'marketing_qualified_leads': 'olist_marketing_qualified_leads_dataset.csv',
        'closed_deals': 'olist_closed_deals_dataset.csv'
    }
    
    # Load all datasets
    print("Loading E-Commerce datasets...")
    ecommerce_data = {}
    for name, filename in ecommerce_files.items():
        try:
            df = pd.read_csv(ecommerce_path / filename)
            ecommerce_data[name] = df
            print(f"✓ {name}: {df.shape[0]:,} rows x {df.shape[1]} cols")
        except FileNotFoundError:
            print(f"✗ {name}: File not found - {filename}")
        except Exception as e:
            print(f"✗ {name}: Error loading - {e}")
    
    print("\nLoading Marketing Funnel datasets...")
    marketing_data = {}
    for name, filename in marketing_files.items():
        try:
            df = pd.read_csv(marketing_path / filename)
            marketing_data[name] = df
            print(f"✓ {name}: {df.shape[0]:,} rows x {df.shape[1]} cols")
        except FileNotFoundError:
            print(f"✗ {name}: File not found - {filename}")
        except Exception as e:
            print(f"✗ {name}: Error loading - {e}")
    
    print(f"\n✅ Data loading complete!")
    print(f"E-Commerce datasets loaded: {len(ecommerce_data)}")
    print(f"Marketing datasets loaded: {len(marketing_data)}")
    
    return ecommerce_data, marketing_data


def main():
    """
    Main function to run the data ingestion process
    """
    print("OLIST DATA INGESTION SCRIPT")
    print("=" * 50)
    print("This script will download and organize Olist datasets from Kaggle")
    print("Ensure you have:")
    print("1. kaggle.json file in the project root")
    print("2. kaggle package installed (pip install kaggle)")
    print("3. Active internet connection")
    print("=" * 50)
    
    # Step 1: Setup and download datasets
    setup_success = setup_kaggle_datasets()
    
    if not setup_success:
        print("\n❌ Setup failed. Please check the error messages above.")
        print("Common solutions:")
        print("1. Ensure kaggle.json exists in the project root")
        print("2. Install kaggle package: pip install kaggle")
        print("3. Check your internet connection")
        print("4. Verify your Kaggle API credentials are valid")
        sys.exit(1)
    
    # Step 2: Load and verify datasets
    try:
        ecommerce_data, marketing_data = load_datasets()
        
        # Quick verification
        total_files = len(ecommerce_data) + len(marketing_data)
        expected_files = 11  # 9 ecommerce + 2 marketing
        
        if total_files == expected_files:
            print(f"\n🎉 SUCCESS! All {expected_files} datasets loaded successfully.")
        else:
            print(f"\n⚠️  Warning: Expected {expected_files} files, but loaded {total_files}")
            
    except Exception as e:
        print(f"\n❌ Error during data loading: {e}")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("Data ingestion completed successfully!")
    print("You can now run your analysis scripts.")
    print("="*50)


if __name__ == "__main__":
    main()
