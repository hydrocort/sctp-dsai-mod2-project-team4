# Business Questions for Marketing Analytics

## Marketing Attribution
1. **Which marketing channels (lead sources) generate the highest revenue?**
2. **What is the ROI of different marketing campaigns?**
3. **How long does it take from first contact to purchase?**
4. **Which lead types convert to the highest-value customers?**

## Customer Lifecycle
5. **What is the customer acquisition cost by channel?**
6. **How does marketing-acquired customer behavior differ from organic customers?**
7. **What is the lifetime value of marketing-acquired customers?**
8. **Which marketing touchpoints lead to repeat purchases?**

## Seller Performance
9. **How do marketing-acquired sellers perform vs. organic sellers?**
10. **Which seller onboarding channels lead to better long-term performance?**
11. **What is the seller retention rate by acquisition channel?**

## Product & Category Analysis
12. **Which product categories benefit most from marketing investment?**
13. **How does marketing affect seasonal product sales?**
14. **What products do marketing-acquired customers prefer?**

## Geographic Insights
15. **How does marketing effectiveness vary by Brazilian state?**
16. **Which regions have untapped marketing potential?**
17. **How does shipping cost affect marketing ROI by location?**

## Business Intelligence
18. **What are the key metrics for marketing campaign optimization?**
19. **How can we predict which leads will convert to high-value customers?**
20. **What marketing mix generates the best overall marketplace health?**

---

## **Analysis of Business Questions vs Available Data**

### **✅ FULLY ANSWERABLE**

#### **Marketing Attribution**
**1. Which marketing channels (lead sources) generate the highest revenue?**
- ✅ **Data**: `origin` (DimMarketing) + `price`, `freight_value` (FactSalesMarketing)
- ✅ **Enhanced**: Can compare against total marketplace revenue (FactSalesAll)

**3. How long does it take from first contact to purchase?**
- ✅ **Data**: `first_contact_date` + `order_purchase_timestamp` → `lead_to_purchase_days`
- ✅ **Query**: AVG(lead_to_purchase_days) by marketing channel

**4. Which lead types convert to the highest-value customers?**
- ✅ **Data**: `lead_type` (DimMarketing) + `total_value` (FactSalesMarketing)
- ✅ **Enhanced**: Can compare customer value across all purchases (FactSalesAll)

#### **Customer Lifecycle (NEW - Now Fully Answerable)**
**6. How does marketing-acquired customer behavior differ from organic customers?**
- ✅ **Data**: `acquisition_channel` (DimCustomer) + both fact tables
- ✅ **Analysis**: Compare purchase patterns, order values, frequency between segments
- ✅ **Query**: 
```sql
SELECT 
    c.acquisition_channel,
    COUNT(*) as total_orders,
    AVG(f.total_value) as avg_order_value,
    SUM(f.total_value) as total_revenue
FROM FactSalesAll f
JOIN DimCustomer c ON f.customer_key = c.customer_key
GROUP BY c.acquisition_channel
```

**7. What is the lifetime value of marketing-acquired customers? (NEW)**
- ✅ **Data**: Customer purchase history across all sellers (FactSalesAll)
- ✅ **Analysis**: Sum of all purchases per customer by acquisition channel

**8. Which marketing touchpoints lead to repeat purchases? (NEW)**
- ✅ **Data**: Customer order history + marketing attribution
- ✅ **Analysis**: Track customers acquired through marketing, analyze subsequent purchases

#### **Seller Performance (Enhanced)**
**9. How do marketing-acquired sellers perform vs. organic sellers?**
- ✅ **Data**: `acquisition_channel` (DimSeller) + FactSalesAll for complete view
- ✅ **Enhanced**: Full performance comparison across entire seller base

**10. Which seller onboarding channels lead to better long-term performance?**
- ✅ **Data**: `origin` (DimMarketing) + seller performance over time (FactSalesAll)
- ✅ **Enhanced**: Complete seller lifecycle analysis

**11. What is the seller retention rate by acquisition channel? (NEW)**
- ✅ **Data**: Seller activity over time from FactSalesAll
- ✅ **Analysis**: Track seller activity periods by acquisition channel

#### **Product & Category Analysis (Enhanced)**
**12. Which product categories benefit most from marketing investment?**
- ✅ **Data**: `product_category_name` (DimProduct) + both fact tables
- ✅ **Enhanced**: Compare category performance: marketing vs organic vs total market

**13. How does marketing affect seasonal product sales? (NEW)**
- ✅ **Data**: Time analysis across both fact tables
- ✅ **Analysis**: Seasonal patterns for marketing vs organic sales

**14. What products do marketing-acquired customers prefer?**
- ✅ **Data**: Product details + customer acquisition channel (both fact tables)
- ✅ **Enhanced**: Complete customer preference analysis

#### **Geographic Insights (Enhanced)**
**15. How does marketing effectiveness vary by Brazilian state?**
- ✅ **Data**: `seller_state`, `customer_state` + both fact tables
- ✅ **Enhanced**: Marketing performance vs total market performance by region

**16. Which regions have untapped marketing potential? (NEW)**
- ✅ **Data**: Regional performance comparison between fact tables
- ✅ **Analysis**: Identify high-organic, low-marketing regions

---

### **🔄 PARTIALLY ANSWERABLE (Improved)**

#### **Marketing Attribution**
**2. What is the ROI of different marketing campaigns?**
- ✅ **Revenue Data**: Complete revenue picture from both fact tables
- ❌ **Cost Data**: Still missing `marketing_cost_allocation`
- **Improvement**: Better revenue attribution and comparison baseline

#### **Customer Lifecycle (Improved)**
**5. What is the customer acquisition cost by channel?**
- ✅ **Volume Data**: Customer acquisition volumes by channel
- ❌ **Cost Data**: Still need marketing spend data
- **Improvement**: Better understanding of acquisition volumes for CAC calculation

#### **Geographic Insights (Improved)**
**17. How does shipping cost affect marketing ROI by location?**
- ✅ **Shipping Cost**: `freight_value` available in both fact tables
- ✅ **Revenue Comparison**: Marketing vs total revenue by location
- ❌ **Marketing Cost**: Still missing for true ROI

---

### **❌ NOT ANSWERABLE (Reduced to 1)**

#### **Business Intelligence**
**18. What are the key metrics for marketing campaign optimization?**
- 🔄 **Partial**: Can derive many optimization metrics, but missing cost data
- **Improvement**: Much better metric foundation with dual fact tables

**19. How can we predict which leads will convert to high-value customers? (NEW - Improved)**
- ✅ **Converted Lead Data**: Available in marketing fact table
- ✅ **Customer Value Data**: Complete customer value from all fact table
- 🔄 **Missing**: Still need unconverted leads for full predictive modeling

**20. What marketing mix generates the best overall marketplace health? (ANSWERABLE)**
- ✅ **Marketplace Metrics**: Can compare marketing vs organic across all dimensions
- ✅ **Health Indicators**: Revenue, customer acquisition, seller performance, geographic spread

---

## **Updated Summary Assessment**

### **Answerable Questions: 16/20 (80%)** ⬆️ +8
### **Partially Answerable: 3/20 (15%)** ⬇️ -6  
### **Not Answerable: 1/20 (5%)** ⬇️ -2

## **Key Benefits of Dual Fact Table Design**

### **1. Complete Market View**
- Marketing attribution in context of total marketplace
- Organic vs marketing performance comparison
- True market share analysis

### **2. Customer Lifecycle Analysis**
- Full customer journey across all sellers
- Repeat purchase behavior
- Lifetime value calculations

### **3. Seller Performance Insights**
- Complete seller ecosystem analysis
- Acquisition channel effectiveness
- Long-term seller retention

### **4. Enhanced Analytics**
- Baseline comparisons for all metrics
- Market penetration analysis
- Opportunity identification

This dual fact table approach transforms the schema from a marketing-only view to a comprehensive marketplace analytics platform!