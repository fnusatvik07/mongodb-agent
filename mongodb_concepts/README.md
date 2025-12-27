# MongoDB Concepts - Simple Examples

Basic MongoDB operations for hotel management system.

## Files

1. **get_collections.py** - List all collections
2. **describe_collection.py** - Show collection structure  
3. **query_orders.py** - Find orders
4. **insert_orders.py** - Add new orders
5. **update_orders.py** - Modify orders
6. **aggregate_data.py** - Group and analyze data
7. **search_orders.py** - Advanced search
8. **revenue_analytics.py** - Calculate revenue
9. **generate_charts.py** - Create data visualizations

## Setup

```bash
# Install
pip install pymongo python-dotenv matplotlib pandas

# Create .env file
echo "MONGO_URI=mongodb://localhost:27017/hotel_management" > .env

# Run any file
python get_collections.py

# Generate charts
python generate_charts.py
```

Each file is standalone - just run and see the results!