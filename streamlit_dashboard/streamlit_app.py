"""
Olist E-commerce Analytics Dashboard
Main application for answering 8 critical business questions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.bigquery_client import init_connection
from utils.data_queries import (
    get_monthly_sales_trends,
    get_top_products_categories,
    get_sales_by_region,
    get_customer_behavior,
    get_payment_analysis,
    get_seller_performance,
    get_reviews_sales_correlation,
    get_delivery_patterns
)
from utils.visualization_helpers import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_metric_card
)

# Page configuration
st.set_page_config(
    page_title="Olist E-commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .tab-content {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">Olist E-commerce Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Dashboard Controls")
        
        # Data refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.success("Cache cleared! Data will refresh on next query.")
        
        st.markdown("---")
        
        # Filter options
        st.subheader("Filters")
        selected_year = st.selectbox(
            "Select Year",
            options=["All Years", "2016", "2017", "2018"],
            index=0
        )
        
        selected_region = st.selectbox(
            "Select Region",
            options=["All Regions", "North", "Northeast", "Southeast", "South", "Central-West"],
            index=0
        )
        
        st.markdown("---")
        
        # Data info
        st.subheader("Data Info")
        st.info("""
        **Last Updated**: Data refreshed from BigQuery marts
        **Data Source**: Olist e-commerce transactions
        **Cache TTL**: 10 minutes
        """)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📈 Monthly Sales Trends",
        "🏷️ Top Products & Categories", 
        "🌍 Geographic Sales Distribution",
        "👥 Customer Purchase Behavior",
        "💳 Payment Method Impact",
        "🏪 Seller Performance Analysis",
        "⭐ Reviews & Sales Correlation",
        "🚚 Delivery Time Patterns"
    ])
    
    # Tab 1: Monthly Sales Trends
    with tab1:
        st.header("Monthly Sales Trends")
        st.markdown("Analyze sales revenue, order volume, and average order values over time")
        
        try:
            # Placeholder for actual data query
            st.info("Data query functions will be implemented in next step")
            
            # Example visualization structure
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Sales", "$2.5M", "↑ 12%")
            with col2:
                st.metric("Total Orders", "99,441", "↑ 8%")
            with col3:
                st.metric("Avg Order Value", "$25.15", "↑ 4%")
            
            # Placeholder chart
            st.plotly_chart(
                go.Figure().add_trace(
                    go.Scatter(x=[], y=[], mode='lines', name='Sales Trend')
                ).update_layout(
                    title="Monthly Sales Trend (Placeholder)",
                    xaxis_title="Month",
                    yaxis_title="Sales ($)",
                    height=400
                ),
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error loading sales trends data: {str(e)}")
    
    # Tab 2: Top Products & Categories
    with tab2:
        st.header("Top Products & Categories")
        st.markdown("Identify highest revenue and sales volume product categories")
        
        try:
            st.info("Product performance analysis will be implemented in next step")
            
            # Placeholder layout
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top Categories by Revenue")
                st.write("Category performance data will be displayed here")
            
            with col2:
                st.subheader("Product Performance")
                st.write("Individual product metrics will be shown here")
                
        except Exception as e:
            st.error(f"Error loading product data: {str(e)}")
    
    # Tab 3: Geographic Sales Distribution
    with tab3:
        st.header("Geographic Sales Distribution")
        st.markdown("Analyze sales patterns across Brazilian regions, states, and cities")
        
        try:
            st.info("Geographic analysis will be implemented in next step")
            
            # Placeholder for regional analysis
            st.write("Regional sales distribution will be visualized here")
            
        except Exception as e:
            st.error(f"Error loading geographic data: {str(e)}")
    
    # Tab 4: Customer Purchase Behavior
    with tab4:
        st.header("Customer Purchase Behavior")
        st.markdown("Understand customer purchasing patterns, frequency, and lifetime value")
        
        try:
            st.info("Customer behavior analysis will be implemented in next step")
            
            # Placeholder for customer insights
            st.write("Customer segmentation and behavior metrics will be displayed here")
            
        except Exception as e:
            st.error(f"Error loading customer data: {str(e)}")
    
    # Tab 5: Payment Method Impact
    with tab5:
        st.header("Payment Method Impact")
        st.markdown("Analyze how payment methods affect sales volumes and order values")
        
        try:
            st.info("Payment analysis will be implemented in next step")
            
            # Placeholder for payment insights
            st.write("Payment method distribution and impact analysis will be shown here")
            
        except Exception as e:
            st.error(f"Error loading payment data: {str(e)}")
    
    # Tab 6: Seller Performance Analysis
    with tab6:
        st.header("Seller Performance Analysis")
        st.markdown("Evaluate seller performance by region and revenue generation")
        
        try:
            st.info("Seller performance analysis will be implemented in next step")
            
            # Placeholder for seller metrics
            st.write("Seller performance metrics and regional analysis will be displayed here")
            
        except Exception as e:
            st.error(f"Error loading seller data: {str(e)}")
    
    # Tab 7: Reviews & Sales Correlation
    with tab7:
        st.header("Product Reviews & Sales Correlation")
        st.markdown("Analyze how customer reviews impact sales performance")
        
        try:
            st.info("Review correlation analysis will be implemented in next step")
            
            # Placeholder for review insights
            st.write("Review score distribution and sales impact analysis will be shown here")
            
        except Exception as e:
            st.error(f"Error loading review data: {str(e)}")
    
    # Tab 8: Delivery Time Patterns
    with tab8:
        st.header("Delivery Time Patterns")
        st.markdown("Examine delivery performance metrics across regions")
        
        try:
            st.info("Delivery pattern analysis will be implemented in next step")
            
            # Placeholder for delivery insights
            st.write("Delivery performance metrics and regional patterns will be displayed here")
            
        except Exception as e:
            st.error(f"Error loading delivery data: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Olist E-commerce Analytics Dashboard | Built with Streamlit & BigQuery"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()





