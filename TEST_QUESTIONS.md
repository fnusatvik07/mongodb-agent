# MongoDB Analytics Agent - Test Questions

This guide provides comprehensive test questions to evaluate the MongoDB Analytics Agent's capabilities across different analytical domains.

## 🔍 Data Exploration Questions

### Basic Database Discovery
```
"Show me all available collections in the database"
"Describe the structure of the orders collection"
"What date range of data is available?"
"How many documents are in each collection?"
"Show me sample data from the customers collection"
```

### Schema Analysis
```
"What fields are available in the orders collection?"
"Describe the menu_items collection structure"
"Show me the data types in the customers collection"
```

## 💰 Revenue Analysis Questions

### Revenue Totals & Summaries
```
"What was the total revenue from September 15-30, 2024?"
"Show me daily revenue breakdown for September 2024"
"What's the average order value?"
"Calculate total revenue for completed orders only"
```

### Revenue Trends
```
"Show daily revenue trends for the last week of September 2024"
"Compare revenue between different order types"
"What's the highest revenue day in September 2024?"
```

### Menu Revenue Analysis
```
"Which menu items generate the most revenue?"
"Show me top 5 dishes by total revenue"
"What's the revenue contribution of each menu category?"
```

## 👥 Customer Analytics Questions

### Top Customers
```
"Who are the top 5 customers by total spending?"
"List the top 10 customers by number of orders"
"Show customers who have spent more than $1000"
```

### Customer Segments
```
"Show me customer segments breakdown"
"List all VIP customers"
"How many customers are in each segment?"
"Which customer segment spends the most on average?"
```

### Customer Behavior
```
"What's the average spending per customer?"
"Which customers order most frequently?"
"Show customer loyalty patterns"
```

## 📦 Order Analysis Questions

### Order Status & Types
```
"How many orders were completed vs cancelled?"
"Show breakdown of order types (dine-in, delivery, takeout)"
"What percentage of orders are successful?"
"List all pending orders"
```

### Order Patterns
```
"What's the most popular order type?"
"Show orders placed on September 15, 2024"
"Find orders with more than 3 items"
"Which day had the most orders?"
```

### Payment Analysis
```
"What payment methods are most popular?"
"Show payment method distribution"
"How much revenue comes from each payment type?"
```

## 🍽️ Menu Performance Questions

### Popular Items
```
"Which 3 menu items are ordered most frequently?"
"Show me the top revenue-generating dishes"
"What's the least popular menu item?"
"List items ordered more than 100 times"
```

### Menu Analytics
```
"What's the average price of menu items?"
"Which items have the highest profit margins?"
"Show menu performance by category"
"Find items that are never ordered"
```

## 📊 Chart Generation Questions

### Revenue Charts
```
"Generate a line chart of daily revenue trends"
"Create a bar chart showing revenue by order type"
"Make a pie chart of payment method distribution"
```

### Customer Charts
```
"Create a bar chart showing top customers by spending"
"Generate a pie chart of customer segments"
"Show a horizontal bar chart of customer order frequency"
```

### Menu Charts
```
"Make a bar chart of top menu items by orders"
"Create a pie chart of menu item revenue distribution"
"Generate a scatter plot of menu item price vs popularity"
```

### Order Charts
```
"Generate a pie chart of order status distribution"
"Create a bar chart comparing order types"
"Show a line chart of orders over time"
```

## 🔎 Advanced Analytics Questions

### Complex Queries
```
"Find orders above $500 in value"
"Show orders from September 15th only"
"Which customer segment spends the most per order?"
"Compare delivery vs dine-in revenue"
```

### Aggregated Analysis
```
"What's the busiest day of the week for orders?"
"Show average order value by customer segment"
"Find customers with unusual ordering patterns"
"Calculate revenue per day for each order type"
```

### Business Intelligence
```
"Which combinations of menu items are ordered together?"
"Show seasonal trends in ordering patterns"
"Identify high-value customer opportunities"
```

## 📋 Summary & Overview Questions

### Business Dashboards
```
"Give me a quick overview of the business"
"Show me key business metrics"
"What are the most important KPIs?"
"Provide a business summary for September 2024"
```

### Performance Metrics
```
"How many total customers do we have?"
"What's our order completion rate?"
"Show overall business performance"
"Calculate key operational metrics"
```

## 🎯 API Testing Examples

### Simple Text Query
```bash
curl -X POST "http://localhost:8001/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me all available collections"}'
```

### Query with Chart Generation
```bash
curl -X POST "http://localhost:8001/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show top 5 customers by spending",
    "generate_chart": true,
    "chart_type": "bar"
  }'
```

### Auto Chart Type Selection
```bash
curl -X POST "http://localhost:8001/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Generate a chart of payment methods breakdown",
    "generate_chart": true,
    "chart_type": "auto"
  }'
```

## 💡 Testing Strategy

### Progressive Testing Approach
1. **Start with Discovery** - Test basic data exploration
2. **Simple Analytics** - Try straightforward queries
3. **Complex Analysis** - Test advanced analytical questions
4. **Chart Generation** - Verify visualization capabilities
5. **Error Handling** - Test with invalid or edge case queries

### Expected Response Format
```json
{
  "success": true,
  "response": "Analysis results...",
  "tool_calls": 2,
  "message_count": 4,
  "tools_used": ["mongodb_query", "get_revenue_analytics"],
  "chart_path": "/charts/chart_20241226_143022.png",
  "chart_title": "Revenue Analysis",
  "chart_type": "bar"
}
```

### Chart Types Available
- `auto` - Automatic selection based on data
- `bar` - Bar charts for comparisons
- `line` - Line charts for trends
- `pie` - Pie charts for distributions
- `horizontal_bar` - Horizontal bar charts
- `scatter` - Scatter plots for correlations

## 🚀 Pro Testing Tips

1. **Use Actual Dates**: Test with September 2024 dates (your actual data range)
2. **Mix Question Types**: Combine simple and complex queries
3. **Test Chart Generation**: Try different chart types for the same data
4. **Validate Results**: Cross-check answers with direct database queries
5. **Error Testing**: Try invalid dates, non-existent collections, etc.
6. **Performance Testing**: Test response times for complex queries

## ⚠️ Common Data Patterns

- **Date Format**: `2024-09-15T14:47:47Z`
- **Order IDs**: `order_00001`, `order_00002`
- **Customer IDs**: `cust_0001`, `cust_0333`
- **Order Status**: `completed`, `cancelled`, `pending`
- **Order Types**: `dine_in`, `delivery`, `takeout`
- **Payment Modes**: `upi`, `card`, `cash`

This comprehensive test suite will help you evaluate all aspects of your MongoDB Analytics Agent! 🎯