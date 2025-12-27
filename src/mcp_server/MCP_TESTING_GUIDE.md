# MCP Server Testing Guide

This guide provides exact test scenarios for all MCP tools. Use these examples in the MCP Inspector to test each tool.

## 🔗 Connection & Discovery Tools

### 1. **mongodb_get_collections**
**Purpose:** List all available collections in the database  
**Parameters:** None  

**Test Example:**
```
No parameters needed - just run the tool
```

**Expected Result:**
```json
{
  "success": true,
  "collections": ["orders", "customers", "menu_items", "users", "audit_logs", "delivery_details"],
  "count": 6
}
```

---

### 2. **mongodb_describe_collection**
**Purpose:** Analyze collection structure and sample data  
**Parameters:**
- `collection`: Collection name
- `sample_size`: Number of sample documents (optional, default: 5)

**Test Example:**
```
collection: orders
sample_size: 3
```

**Expected Result:** Schema information, sample documents, and field statistics

---

## 📊 Basic Query Tools

### 3. **mongodb_query**
**Purpose:** Find and filter documents with basic queries  
**Parameters:**
- `collection`: Collection name
- `query`: Query filter (optional, default: None for all documents)
- `limit`: Number of results (optional, default: 10)

**Test Examples:**

**Example 3a - All Orders:**
```
collection: orders
query: {}
limit: 5
```

**Example 3b - Completed Orders:**
```
collection: orders
query: {"order_status": "completed"}
limit: 3
```

**Example 3c - High Value Orders:**
```
collection: orders
query: {"total_amount": {"$gt": 600}}
limit: 5
```

**Example 3d - Delivery Orders:**
```
collection: orders
query: {"order_type": "delivery"}
limit: 3
```

**Example 3e - UPI Payments:**
```
collection: orders
query: {"payment_mode": "upi"}
limit: 3
```

---

### 4. **search_orders_by_criteria**
**Purpose:** Advanced search with multiple criteria filters  
**Parameters:**
- `customer_segment`: Customer segment filter (optional)
- `order_type`: Order type filter (optional)
- `status`: Status filter (optional)
- `min_amount`: Minimum amount (optional)
- `max_amount`: Maximum amount (optional)
- `start_date`: Start date YYYY-MM-DD (optional)
- `end_date`: End date YYYY-MM-DD (optional)
- `limit`: Number of results (optional, default: 10)

**Test Examples:**

**Example 4a - Search by Order Type:**
```
order_type: delivery
limit: 5
```

**Example 4b - Search by Amount Range:**
```
min_amount: 500
max_amount: 1000
limit: 5
```

**Example 4c - Search by Date Range:**
```
start_date: 2024-09-15
end_date: 2024-09-16
limit: 5
```

**Example 4d - Search VIP Customers:**
```
customer_segment: vip
limit: 3
```

---

## 📈 Aggregation & Analytics Tools

### 5. **mongodb_aggregate**
**Purpose:** Complex data analysis with aggregation pipelines  
**Parameters:**
- `collection`: Collection name
- `pipeline`: List of aggregation stages

**Test Examples:**

**Example 5a - Revenue by Status:**
```
collection: orders
pipeline: [
  {
    "$match": {
      "order_status": "completed"
    }
  },
  {
    "$group": {
      "_id": "$order_status",
      "total_revenue": {
        "$sum": "$total_amount"
      },
      "order_count": {
        "$sum": 1
      }
    }
  }
]
```

**Example 5b - Top 5 Customers by Order Count:**
```
collection: orders
pipeline: [
  {
    "$match": {
      "order_status": "completed"
    }
  },
  {
    "$group": {
      "_id": "$customer_id",
      "total_orders": {
        "$sum": 1
      },
      "total_spent": {
        "$sum": "$total_amount"
      }
    }
  },
  {
    "$sort": {
      "total_orders": -1
    }
  },
  {
    "$limit": 5
  }
]
```

**Example 5c - Daily Revenue for September:**
```
collection: orders
pipeline: [
  {
    "$match": {
      "order_status": "completed",
      "created_at": {
        "$regex": "^2024-09"
      }
    }
  },
  {
    "$addFields": {
      "order_date": {
        "$substr": [
          "$created_at",
          0,
          10
        ]
      }
    }
  },
  {
    "$group": {
      "_id": "$order_date",
      "daily_revenue": {
        "$sum": "$total_amount"
      },
      "order_count": {
        "$sum": 1
      }
    }
  },
  {
    "$sort": {
      "_id": 1
    }
  }
]
```

---

## 💼 Revenue Analytics Tools

### 6. **get_daily_revenue**
**Purpose:** Get daily revenue breakdown for specific date range  
**Parameters:**
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

**Test Examples:**

**Example 6a - Week Range:**
```
start_date: 2024-09-15
end_date: 2024-09-21
```

**Example 6b - Single Day:**
```
start_date: 2024-09-15
end_date: 2024-09-15
```

---

### 7. **get_revenue_by_date_range**
**Purpose:** Get total revenue statistics for date range  
**Parameters:**
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

**Test Example:**
```
start_date: 2024-09-15
end_date: 2024-09-30
```

---

## 👥 Customer Analytics Tools

### 8. **get_top_customers_by_spending**
**Purpose:** Get customers ranked by total spending  
**Parameters:**
- `limit`: Number of top customers (optional, default: 10)

**Test Examples:**

**Example 8a - Top 5 Customers:**
```
limit: 5
```

**Example 8b - Top 10 Customers (default):**
```
No parameters (uses default limit=10)
```

---

### 9. **get_customer_segments**
**Purpose:** Analyze customer segments and their behavior  
**Parameters:** None

**Test Example:**
```
No parameters needed
```

**Expected Result:** Customer segment analysis with counts and spending patterns

---

## 📦 Order Analytics Tools

### 10. **get_orders_by_status**
**Purpose:** Order status distribution analysis  
**Parameters:** None

**Test Example:**
```
No parameters needed
```

**Expected Result:** Breakdown of orders by status (completed, cancelled, pending, etc.)

---

### 11. **get_orders_by_type**
**Purpose:** Order type analysis (dine_in, takeout, delivery)  
**Parameters:** None

**Test Example:**
```
No parameters needed
```

**Expected Result:** Distribution of orders by type with counts and percentages

---

## 🍽️ Menu Analytics Tools

### 12. **get_top_menu_items_by_orders**
**Purpose:** Most frequently ordered menu items  
**Parameters:**
- `limit`: Number of top items (optional, default: 10)

**Test Examples:**

**Example 12a - Top 5 Items:**
```
limit: 5
```

**Example 12b - Top 10 Items (default):**
```
No parameters (uses default limit=10)
```

---

### 13. **get_top_menu_items_by_revenue**
**Purpose:** Menu items generating highest revenue  
**Parameters:**
- `limit`: Number of top items (optional, default: 10)

**Test Examples:**

**Example 13a - Top 3 Revenue Items:**
```
limit: 3
```

**Example 13b - Top 10 Revenue Items (default):**
```
No parameters (uses default limit=10)
```

---

## 💳 Payment Analytics Tools

### 14. **get_payment_methods_breakdown**
**Purpose:** Payment method distribution analysis  
**Parameters:** None

**Test Example:**
```
No parameters needed
```

**Expected Result:** Breakdown by payment method (upi, card, cash) with counts

---

## 📊 Summary & Statistics Tools

### 15. **get_collection_summary**
**Purpose:** Summary statistics for any collection  
**Parameters:**
- `collection`: Collection name

**Test Examples:**

**Example 15a - Orders Summary:**
```
collection: orders
```

**Example 15b - Customers Summary:**
```
collection: customers
```

**Example 15c - Menu Items Summary:**
```
collection: menu_items
```

---

### 16. **get_data_date_range**
**Purpose:** Get available data date range  
**Parameters:**
- `collection`: Collection name (optional, default: "orders")

**Test Examples:**

**Example 16a - Orders Date Range:**
```
collection: orders
```

**Example 16b - Default Collection:**
```
No parameters (uses default collection=orders)
```

---

## 🛠️ Data Modification Tools

### 17. **mongodb_insert**
**Purpose:** Insert new documents into collections  
**Parameters:**
- `collection`: Collection name
- `document`: Single document dict or list of document dicts

**Test Examples:**

**Example 17a - Single Order:**
```
collection: orders
document: {
  "_id": "test_order_001",
  "customer_id": "cust_0001",
  "total_amount": 299.50,
  "order_status": "pending",
  "order_type": "dine_in",
  "created_at": "2024-12-26T12:00:00Z",
  "payment_mode": "upi",
  "items": [
    {
      "item_id": "item_001",
      "name": "Test Burger",
      "qty": 1,
      "price": 299.50
    }
  ]
}
```

**Example 17b - Multiple Documents:**
```
collection: orders
document: [
  {
    "_id": "test_order_002",
    "customer_id": "cust_0002",
    "total_amount": 150.00,
    "order_status": "completed",
    "order_type": "takeout",
    "created_at": "2024-12-26T11:00:00Z",
    "payment_mode": "card"
  },
  {
    "_id": "test_order_003", 
    "customer_id": "cust_0003",
    "total_amount": 450.75,
    "order_status": "pending",
    "order_type": "delivery",
    "created_at": "2024-12-26T13:00:00Z",
    "payment_mode": "cash"
  }
]
```

---

### 18. **mongodb_update**
**Purpose:** Update existing documents  
**Parameters:**
- `collection`: Collection name
- `filter_criteria`: Filter to find documents
- `update_data`: Update operations
- `upsert`: Create if not found (optional, default: false)

**Test Examples:**

**Example 18a - Update Order Status:**
```
collection: orders
filter_criteria: {"_id": "test_order_001"}
update_data: {
  "$set": {
    "order_status": "completed",
    "timestamps.completed": "2024-12-26T13:00:00Z"
  }
}
upsert: false
```

**Example 18b - Update Customer Info:**
```
collection: customers
filter_criteria: {"_id": "cust_0001"}
update_data: {
  "$inc": {
    "total_orders": 1,
    "total_spent": 299.50
  }
}
upsert: false
```

---

## 📊 Visualization Tools

### 19. **generate_chart_from_data**
**Purpose:** Create data visualizations  
**Parameters:**
- `data_source`: Data source for chart
- `chart_type`: Type of chart (optional, default: "bar")
- `title`: Chart title (optional)
- `x_field`: X-axis field (optional)
- `y_field`: Y-axis field (optional)
- `limit`: Number of data points (optional, default: 10)
- `start_date`: Start date YYYY-MM-DD (optional)
- `end_date`: End date YYYY-MM-DD (optional)

**Test Examples:**

**Example 19a - Revenue by Type Bar Chart:**
```
data_source: revenue_by_order_type
chart_type: bar
title: Revenue Distribution by Order Type
limit: 5
```

**Example 19b - Customer Segments Pie Chart:**
```
data_source: customer_segments
chart_type: pie
title: Customer Segment Distribution
```

**Example 19c - Daily Revenue Line Chart:**
```
data_source: daily_revenue
chart_type: line
title: Daily Revenue Trend
start_date: 2024-09-15
end_date: 2024-09-30
```

---

## 🎯 Testing Workflow

### **Recommended Testing Order:**

1. **Start with Discovery:**
   - `mongodb_get_collections` → See what's available
   - `mongodb_describe_collection` → Understand data structure

2. **Basic Queries:**
   - `mongodb_query` → Simple filtering
   - `search_orders_by_criteria` → Advanced search patterns

3. **Analytics Foundation:**
   - `get_collection_summary` → Basic statistics
   - `get_data_date_range` → Available date range

4. **Revenue Analytics:**
   - `get_daily_revenue` → Daily breakdowns
   - `get_revenue_by_date_range` → Period totals

5. **Business Analytics:**
   - `get_orders_by_status` → Order status distribution
   - `get_orders_by_type` → Order type analysis
   - `get_customer_segments` → Customer analysis
   - `get_top_customers_by_spending` → Top customers
   - `get_payment_methods_breakdown` → Payment analysis

6. **Menu Analytics:**
   - `get_top_menu_items_by_orders` → Popular items
   - `get_top_menu_items_by_revenue` → Revenue items

7. **Advanced Analysis:**
   - `mongodb_aggregate` → Custom analysis

8. **Visualization:**
   - `generate_chart_from_data` → Create visualizations

9. **Data Modification:**
   - `mongodb_insert` → Add test data
   - `mongodb_update` → Modify test data

### **Tips for Testing:**
- ✅ Always test simple examples first
- ✅ Copy-paste the JSON exactly as shown  
- ✅ Start with tools that don't require parameters
- ✅ Use discovery tools first to understand your data
- ✅ Check date ranges with `get_data_date_range` before filtering by dates
- ✅ Use reasonable limits (3-10) for initial testing

### **Common Field Names in Data:**
- `_id` - Document ID (e.g., "order_00001", "cust_0001")
- `order_status` - Order status (completed, cancelled, pending)
- `customer_id` - Customer reference (e.g., "cust_0333")
- `total_amount` - Order total (numeric)
- `created_at` - Creation timestamp (ISO format)
- `order_type` - Type (dine_in, delivery, takeout)
- `payment_mode` - Payment method (upi, card, cash)
- `items` - Array of ordered items
- `segment` - Customer segment (regular, vip, standard)

### **Date Format Guidelines:**
- All dates use `YYYY-MM-DD` format for parameters
- Database dates are in ISO format: `2024-09-15T14:47:47Z`
- Available data range: September 2024 (use `get_data_date_range` to confirm)

### **Error Prevention:**
- ❌ Don't use non-existent field names
- ❌ Don't use wrong date formats  
- ❌ Don't set unrealistic limits (>1000)
- ❌ Don't skip discovery tools when working with new collections

**This guide covers all 19 MCP tools with exact test parameters for comprehensive candidate evaluation!**