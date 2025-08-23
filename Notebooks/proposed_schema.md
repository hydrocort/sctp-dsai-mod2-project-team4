
## Star Schema Detailed Breakdown

### **FACT TABLE: FactSales**

**Grain**: One row per order item from ALL sellers (marketing + organic)
**Source**: Full e-commerce datasets

#### **Fact Attributes**
| Column | Source Dataset | Available in Full Data |
|--------|----------------|------------------------|
| `order_id` | orders | ✅ Available |
| `order_item_id` | order_items | ✅ Available |
| `shipping_limit_date` | order_items | ✅ Available |

#### **Core Measures (Quantitative Data)**
| Column | Source Dataset | Available in Full Data |
|--------|----------------|------------------------|
| `price` | order_items | ✅ Available |
| `freight_value` | order_items | ✅ Available |
| `total_value` | Calculated (price + freight) | 🔄 Needs calculation |
| `lead_to_purchase_days` | Calculated from dates | 🔄 Only for marketing records |
| `marketing_cost_allocation` | External cost data | ❌ Not available |

#### **Foreign Keys to Dimensions**
- `customer_key` → Links to DimCustomer
- `product_key` → Links to DimProduct  
- `seller_key` → Links to DimSeller
- `order_date_key` → Links to DimDate
- `mql_key` → Links to DimMarketing (NULL for organic)
- `payment_key` → Links to DimPayment

### **Lead to Purchase Days Calculation Logic:**
```python
def calculate_lead_to_purchase_days(combined_dataset):
    if 'first_contact_date' in combined_dataset.columns and 'order_purchase_timestamp' in combined_dataset.columns:
        # Convert to datetime if not already
        first_contact = pd.to_datetime(combined_dataset['first_contact_date'])
        purchase_timestamp = pd.to_datetime(combined_dataset['order_purchase_timestamp'])
        
        # Calculate difference in days
        lead_to_purchase_days = (purchase_timestamp - first_contact).dt.days
        
        return lead_to_purchase_days
    else:
        # Return NaN series if required columns are missing
```
    

---

### **DIMENSION TABLES**

## **1. DimCustomer (Enhanced)**

| Column | Source Dataset | Logic | Available |
|--------|----------------|-------|-----------|
| `customer_key` | Generated surrogate key | 🔄 New PK | - |
| `customer_id` | customers | Natural key | ✅ Available |
| `customer_unique_id` | customers | Business key | ✅ Available |
| `customer_zip_code_prefix` | customers | Geographic | ✅ Available |
| `customer_city` | customers | Geographic | ✅ Available |
| `customer_state` | customers | Geographic | ✅ Available |
| `acquisition_channel` | **Enhanced Business Logic** | **Multi-level derivation** | 🔄 **Enhanced** |

### **Enhanced Customer Acquisition Channel Logic:**
```python
def derive_customer_acquisition_channel(customer_id, all_orders, marketing_sellers):
    customer_orders = all_orders[all_orders['customer_id'] == customer_id]
    
    # Check if ANY order was from marketing-attributed seller
    marketing_orders = customer_orders[customer_orders['seller_id'].isin(marketing_sellers)]
    
    if len(marketing_orders) > 0:
        # Further categorize by first marketing touchpoint
        first_marketing_order = marketing_orders.sort_values('order_purchase_timestamp').iloc[0]
        return f"marketing_{first_marketing_order['origin']}"  # e.g., "marketing_paid_search"
    else:
        return 'organic'
```

## **2. DimSeller (Enhanced)**

| Column | Source Dataset | Logic | Available |
|--------|----------------|-------|-----------|
| `seller_key` | Generated surrogate key | 🔄 New PK | - |
| `seller_id` | sellers | Natural key | ✅ Available |
| `seller_zip_code_prefix` | sellers | Geographic | ✅ Available |
| `seller_city` | sellers | Geographic | ✅ Available |
| `seller_state` | sellers | Geographic | ✅ Available |
| `acquisition_channel` | **Enhanced Business Logic** | **Clear categorization** | 🔄 **Enhanced** |
| `mql_id` | marketing data | Marketing attribution | 🔄 NULL for organic |
| `deal_close_date` | closed_deals | Marketing timeline | 🔄 NULL for organic |

### **Enhanced Seller Acquisition Channel Logic:**
```python
def derive_seller_acquisition_channel(seller_id, marketing_sellers_dict):
    if seller_id in marketing_sellers_dict:
        # Get marketing details
        marketing_info = marketing_sellers_dict[seller_id]
        return f"marketing_{marketing_info['origin']}"  # e.g., "marketing_social_media"
    else:
        return 'organic'
```

## **3. DimProduct**

| Column | Source Dataset | Available in Source Data |
|--------|----------------|--------------------------|
| `product_key` | Generated surrogate key | 🔄 New PK |
| `product_id` | products | ✅ Available |
| `product_category_name` | products | ✅ Available |
| `product_name_length` | products | ✅ Available |
| `product_description_length` | products | ✅ Available |
| `product_photos_qty` | products | ✅ Available |
| `product_weight_g` | products | ✅ Available |
| `product_length_cm` | products | ✅ Available |
| `product_height_cm` | products | ✅ Available |
| `product_width_cm` | products | ✅ Available |

## **4. DimDate**

| Column | Source Dataset | Available in Source Data |
|--------|----------------|--------------------------|
| `date_key` | Generated surrogate key | 🔄 New PK |
| `order_purchase_timestamp` | orders | ✅ Available |
| `order_approved_at` | orders | ✅ Available |
| `order_delivered_carrier_date` | orders | ✅ Available |
| `order_delivered_customer_date` | orders | ✅ Available |
| `order_estimated_delivery_date` | orders | ✅ Available |
| `first_contact_date` | marketing_qualified_leads | ✅ Available |
| `deal_close_date` | closed_deals | ✅ Available |

## **5. DimGeography**

| Column | Source Dataset | Available in Source Data |
|--------|----------------|--------------------------|
| `geography_key` | Generated surrogate key | 🔄 New PK |
| `zip_code_prefix` | customers/sellers | ✅ Available |
| `city` | customers/sellers | ✅ Available |
| `state` | customers/sellers | ✅ Available |
| `geolocation_lat` | geolocation | ✅ Available |
| `geolocation_lng` | geolocation | ✅ Available |

## **6. DimPayment**

| Column | Source Dataset | Available in Source Data |
|--------|----------------|--------------------------|
| `payment_key` | Generated surrogate key | 🔄 New PK |
| `payment_type` | order_payments | ✅ Available |
| `payment_installments` | order_payments | ✅ Available |
| `payment_value` | order_payments | ✅ Available |

## **7. DimMarketing**

| Column | Source Dataset | Available in Source Data |
|--------|----------------|--------------------------|
| `marketing_key` | Generated surrogate key | 🔄 New PK |
| `mql_id` | marketing_qualified_leads | ✅ Available |
| `lead_type` | closed_deals | ✅ Available |
| `lead_behaviour_profile` | closed_deals | ✅ Available |
| `origin` | marketing_qualified_leads | ✅ Available |
| `first_contact_date` | marketing_qualified_leads | ✅ Available |
| `landing_page_id` | marketing_qualified_leads | ✅ Available |
| `business_segment` | closed_deals | ✅ Available |
| `business_type` | closed_deals | ✅ Available |

## **8. DimProductCategory**

| Column | Source Dataset | Available in Source Data |
|--------|----------------|--------------------------|
| `category_key` | Generated surrogate key | 🔄 New PK |
| `product_category_name` | products | ✅ Available |
| `product_category_name_english` | category_translation | ✅ Available |
| `category_group` | Business logic | 🔄 Custom groupings |

---

## **Key Insights**
## **Key Insights**

### **What's Ready to Use** ✅
- **Dual Fact Tables**: Complete marketplace view (all sales) + focused marketing attribution
- **Enhanced Dimensions**: Customer and seller acquisition channels with full attribution
- **Complete Product Data**: All product details and categories available
- **Full Geographic Coverage**: All location data including coordinates available
- **Payment Information**: Complete payment details for all transactions
- **Marketing Attribution**: Full marketing funnel data for attributed sales
- **Date Hierarchy**: Comprehensive time dimensions for all business events

### **What Needs to Be Added** 🔄
- **Surrogate Keys**: Generate primary keys for all dimension tables
- **Calculated Measures**: 
  - `total_value` (price + freight) for both fact tables
  - `lead_to_purchase_days` for marketing-attributed sales
- **Derived Fields**: 
  - Enhanced `acquisition_channel` logic for customers and sellers
  - `category_group` custom business groupings

### **What's Still Missing** ❌
- **Marketing Cost Data**: External cost allocation for true ROI analysis
- **Campaign Details**: Granular campaign information for optimization
- **Unconverted Leads**: Lead data that didn't convert to deals (for predictive modeling)

### **Implementation next step phases**

**Phase 2: Advanced Analytics (Medium Term)**
- Add marketing cost allocation
- Implement predictive modeling features
- Create advanced geographic and temporal analytics

**Phase 3: Complete Intelligence (Long Term)**
- Integrate external market data
- Add real-time campaign tracking
- Implement AI-driven optimization recommendations

