"""
Data Query Functions for Olist Analytics Dashboard
Implements queries for all 8 critical business questions using BigQuery marts
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, Tuple
from .bigquery_client import execute_query, init_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_data(ttl=600)
def get_monthly_sales_trends(year_filter: Optional[str] = None) -> pd.DataFrame:
    """
    Get monthly sales trends data for business question 1
    
    Args:
        year_filter (str, optional): Filter by specific year
        
    Returns:
        pd.DataFrame: Monthly sales metrics with columns:
            - month_year: Month and year
            - total_orders: Number of orders
            - total_sales: Total sales revenue
            - avg_order_value: Average order value
            - total_items: Total items sold
    """
    try:
        # Build query with optional year filter
        year_condition = f"AND d.year = {year_filter}" if year_filter and year_filter != "All Years" else ""
        
        query = f"""
        SELECT 
            FORMAT_DATE('%Y-%m', d.full_date) as month_year,
            d.year,
            d.month,
            d.month_name,
            COUNT(DISTINCT f.order_key) as total_orders,
            COUNT(f.order_item_sk) as total_items,
            ROUND(SUM(f.total_item_value), 2) as total_sales,
            ROUND(SUM(f.payment_value), 2) as total_payments,
            ROUND(AVG(f.total_item_value), 2) as avg_order_value,
            ROUND(AVG(f.payment_value), 2) as avg_payment_value
        FROM `olist_marts.fact_sales` f
        JOIN `olist_marts.dim_date` d ON f.date_key = d.date_key
        WHERE 1=1 {year_condition}
        GROUP BY d.year, d.month, d.month_name, d.full_date
        ORDER BY d.year, d.month
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get monthly sales trends: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_top_products_categories(limit: int = 20) -> pd.DataFrame:
    """
    Get top products and categories performance for business question 2
    
    Args:
        limit (int): Number of top categories to return
        
    Returns:
        pd.DataFrame: Category performance metrics
    """
    try:
        query = f"""
        SELECT 
            p.product_category_english as category,
            COUNT(DISTINCT p.product_key) as unique_products,
            COUNT(f.order_item_sk) as items_sold,
            ROUND(SUM(f.total_item_value), 2) as total_revenue,
            ROUND(AVG(f.total_item_value), 2) as avg_item_value,
            ROUND(SUM(f.freight_value), 2) as total_freight
        FROM `olist_marts.fact_sales` f
        JOIN `olist_marts.dim_products` p ON f.product_key = p.product_key
        WHERE p.product_category_english IS NOT NULL
        GROUP BY p.product_category_english
        ORDER BY total_revenue DESC
        LIMIT {limit}
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get top products categories: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_sales_by_region() -> pd.DataFrame:
    """
    Get geographic sales distribution for business question 3
    
    Returns:
        pd.DataFrame: Regional sales metrics for customers and sellers
    """
    try:
        query = """
        SELECT 
            c.customer_region,
            s.seller_region,
            COUNT(DISTINCT f.order_key) as total_orders,
            COUNT(f.order_item_sk) as total_items,
            ROUND(SUM(f.total_item_value), 2) as total_sales,
            ROUND(AVG(f.total_item_value), 2) as avg_order_value,
            COUNT(DISTINCT c.customer_key) as unique_customers,
            COUNT(DISTINCT s.seller_key) as unique_sellers
        FROM `olist_marts.fact_sales` f
        JOIN `olist_marts.dim_customers` c ON f.customer_key = c.customer_key
        JOIN `olist_marts.dim_sellers` s ON f.seller_key = s.seller_key
        WHERE c.customer_region IS NOT NULL AND s.seller_region IS NOT NULL
        GROUP BY c.customer_region, s.seller_region
        ORDER BY total_sales DESC
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get sales by region: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_customer_behavior() -> pd.DataFrame:
    """
    Get customer purchase behavior analysis for business question 4
    
    Returns:
        pd.DataFrame: Customer behavior metrics and segments
    """
    try:
        query = """
        WITH customer_metrics AS (
            SELECT 
                c.customer_key,
                c.customer_region,
                COUNT(DISTINCT f.order_key) as order_count,
                ROUND(SUM(f.total_item_value), 2) as total_spent,
                ROUND(AVG(f.total_item_value), 2) as avg_order_value,
                DATE_DIFF(MAX(d.full_date), MIN(d.full_date), DAY) as customer_lifetime_days
            FROM `olist_marts.fact_sales` f
            JOIN `olist_marts.dim_customers` c ON f.customer_key = c.customer_key
            JOIN `olist_marts.dim_date` d ON f.date_key = d.date_key
            GROUP BY c.customer_key, c.customer_region
        )
        SELECT 
            customer_region,
            COUNT(*) as customer_count,
            ROUND(AVG(order_count), 1) as avg_orders_per_customer,
            ROUND(AVG(total_spent), 2) as avg_customer_lifetime_value,
            ROUND(AVG(avg_order_value), 2) as avg_order_value,
            ROUND(AVG(customer_lifetime_days), 1) as avg_customer_lifetime_days,
            SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END) as one_time_customers,
            SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) as repeat_customers
        FROM customer_metrics
        GROUP BY customer_region
        ORDER BY avg_customer_lifetime_value DESC
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get customer behavior: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_payment_analysis() -> pd.DataFrame:
    """
    Get payment method impact analysis for business question 5
    
    Returns:
        pd.DataFrame: Payment method usage and impact metrics
    """
    try:
        query = """
        SELECT 
            p.primary_payment_type,
            COUNT(DISTINCT f.order_key) as total_orders,
            ROUND(SUM(f.total_item_value), 2) as total_sales,
            ROUND(AVG(f.total_item_value), 2) as avg_order_value,
            ROUND(AVG(p.total_installments), 1) as avg_installments,
            SUM(CASE WHEN p.uses_credit_card THEN 1 ELSE 0 END) as credit_card_orders,
            SUM(CASE WHEN p.uses_boleto THEN 1 ELSE 0 END) as boleto_orders,
            SUM(CASE WHEN p.uses_voucher THEN 1 ELSE 0 END) as voucher_orders,
            ROUND(SUM(f.payment_value), 2) as total_payments
        FROM `olist_marts.fact_sales` f
        JOIN `olist_marts.dim_payments` p ON f.payment_key = p.payment_key
        GROUP BY p.primary_payment_type
        ORDER BY total_sales DESC
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get payment analysis: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_seller_performance() -> pd.DataFrame:
    """
    Get seller performance analysis for business question 6
    
    Returns:
        pd.DataFrame: Seller performance metrics by region
    """
    try:
        query = """
        SELECT 
            s.seller_region,
            COUNT(DISTINCT s.seller_key) as unique_sellers,
            COUNT(DISTINCT f.order_key) as total_orders,
            COUNT(f.order_item_sk) as total_items,
            ROUND(SUM(f.total_item_value), 2) as total_revenue,
            ROUND(AVG(f.total_item_value), 2) as avg_item_value,
            ROUND(SUM(f.total_item_value) / COUNT(DISTINCT s.seller_key), 2) as revenue_per_seller,
            COUNT(DISTINCT f.product_key) as unique_products_sold
        FROM `olist_marts.fact_sales` f
        JOIN `olist_marts.dim_sellers` s ON f.seller_key = s.seller_key
        WHERE s.seller_region IS NOT NULL
        GROUP BY s.seller_region
        ORDER BY total_revenue DESC
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get seller performance: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_reviews_sales_correlation() -> pd.DataFrame:
    """
    Get reviews and sales correlation analysis for business question 7
    
    Returns:
        pd.DataFrame: Review impact on sales performance
    """
    try:
        query = """
        SELECT 
            CASE 
                WHEN r.review_key IS NULL THEN 'No Review'
                WHEN r.review_score >= 4 THEN 'Positive (4-5)'
                WHEN r.review_score = 3 THEN 'Neutral (3)'
                ELSE 'Negative (1-2)'
            END as review_category,
            COUNT(f.order_item_sk) as total_items,
            ROUND(SUM(f.total_item_value), 2) as total_sales,
            ROUND(AVG(f.total_item_value), 2) as avg_item_value,
            ROUND(AVG(COALESCE(r.review_score, 0)), 1) as avg_review_score,
            COUNT(r.review_key) as reviews_count,
            COUNT(*) - COUNT(r.review_key) as no_review_count
        FROM `olist_marts.fact_sales` f
        LEFT JOIN `olist_marts.dim_reviews` r ON f.review_key = r.review_key
        GROUP BY 
            CASE 
                WHEN r.review_key IS NULL THEN 'No Review'
                WHEN r.review_score >= 4 THEN 'Positive (4-5)'
                WHEN r.review_score = 3 THEN 'Neutral (3)'
                ELSE 'Negative (1-2)'
            END
        ORDER BY total_sales DESC
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get reviews sales correlation: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_delivery_patterns() -> pd.DataFrame:
    """
    Get delivery time patterns analysis for business question 8
    
    Returns:
        pd.DataFrame: Delivery performance metrics by region
    """
    try:
        query = """
        SELECT 
            c.customer_region,
            COUNT(DISTINCT f.order_key) as total_orders,
            ROUND(AVG(o.days_to_delivery), 1) as avg_delivery_days,
            ROUND(AVG(o.delivery_vs_estimate_days), 1) as avg_delivery_vs_estimate,
            SUM(CASE WHEN o.is_delivered_on_time THEN 1 ELSE 0 END) as on_time_deliveries,
            SUM(CASE WHEN NOT o.is_delivered_on_time THEN 1 ELSE 0 END) as late_deliveries,
            ROUND(
                SUM(CASE WHEN o.is_delivered_on_time THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
                1
            ) as on_time_delivery_rate,
            ROUND(MIN(o.days_to_delivery), 1) as min_delivery_days,
            ROUND(MAX(o.days_to_delivery), 1) as max_delivery_days
        FROM `olist_marts.fact_sales` f
        JOIN `olist_marts.dim_orders` o ON f.order_key = o.order_key
        JOIN `olist_marts.dim_customers` c ON f.customer_key = c.customer_key
        WHERE o.days_to_delivery IS NOT NULL
        GROUP BY c.customer_region
        ORDER BY avg_delivery_days ASC
        """
        
        return execute_query(query)
        
    except Exception as e:
        logger.error(f"Failed to get delivery patterns: {str(e)}")
        return pd.DataFrame()

def get_dashboard_summary() -> Dict[str, Any]:
    """
    Get summary metrics for dashboard overview
    
    Returns:
        Dict: Summary metrics for all business areas
    """
    try:
        # Get basic counts and totals
        summary_query = """
        SELECT 
            COUNT(DISTINCT f.order_key) as total_orders,
            COUNT(f.order_item_sk) as total_items,
            ROUND(SUM(f.total_item_value), 2) as total_sales,
            ROUND(AVG(f.total_item_value), 2) as avg_order_value,
            COUNT(DISTINCT f.customer_key) as unique_customers,
            COUNT(DISTINCT f.seller_key) as unique_sellers,
            COUNT(DISTINCT f.product_key) as unique_products
        FROM `olist_marts.fact_sales` f
        """
        
        summary_df = execute_query(summary_query)
        
        if len(summary_df) > 0:
            return {
                'total_orders': int(summary_df.iloc[0]['total_orders']),
                'total_items': int(summary_df.iloc[0]['total_items']),
                'total_sales': float(summary_df.iloc[0]['total_sales']),
                'avg_order_value': float(summary_df.iloc[0]['avg_order_value']),
                'unique_customers': int(summary_df.iloc[0]['unique_customers']),
                'unique_sellers': int(summary_df.iloc[0]['unique_sellers']),
                'unique_products': int(summary_df.iloc[0]['unique_products'])
            }
        else:
            return {}
            
    except Exception as e:
        logger.error(f"Failed to get dashboard summary: {str(e)}")
        return {}

def validate_marts_data() -> Dict[str, bool]:
    """
    Validate that all required marts tables exist and have data
    
    Returns:
        Dict: Validation status for each table
    """
    required_tables = [
        'fact_sales',
        'dim_customers', 
        'dim_products',
        'dim_sellers',
        'dim_orders',
        'dim_payments',
        'dim_reviews',
        'dim_date'
    ]
    
    validation_results = {}
    
    for table in required_tables:
        try:
            query = f"SELECT COUNT(*) as count FROM `olist_marts.{table}`"
            result = execute_query(query)
            validation_results[table] = len(result) > 0 and result.iloc[0]['count'] > 0
        except Exception as e:
            logger.error(f"Failed to validate table {table}: {str(e)}")
            validation_results[table] = False
    
    return validation_results





