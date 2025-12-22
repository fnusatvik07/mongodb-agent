"""
MongoDB Hotel Analytics MCP Server
Main server implementation using FastMCP
"""

import logging
import os
import sys
from fastmcp import FastMCP

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mcp_server.utils.db_client import mongo_client

# Import all tools
from tools import mongodb_query
from tools import mongodb_aggregate
from tools import mongodb_insert
from tools import mongodb_update
from tools import mongodb_get_collections
from tools import mongodb_describe_collection
from tools import get_revenue_analytics
from tools import get_customer_insights
from tools import get_menu_performance
from tools import get_operational_metrics
from tools import quick_stats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server - available for tools to import
mcp = FastMCP("mongodb-hotel-analytics")

# Tool definitions
@mcp.tool()
def mongodb_query(
    collection: str,
    query: Dict[str, Any] = {},
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Execute a MongoDB find query
    
    Args:
        collection: Collection name
        query: Query filter (default: {} for all)
        limit: Max documents to return
        
    Examples:
        - mongodb_query("orders")
        - mongodb_query("customers", {"segment": "vip"})
    """
    start_time = time.time()
    
    try:
        result = mongo_client.execute_query(collection, query, limit)
        execution_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "data": result,
            "count": len(result),
            "execution_time_ms": round(execution_time, 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2)
        }

@mcp.tool()
def mongodb_aggregate(
    collection: str,
    pipeline: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Execute MongoDB aggregation pipeline
    
    Args:
        collection: Collection name
        pipeline: List of aggregation stages
        
    Examples:
        - Daily revenue: mongodb_aggregate("orders", [
            {"$group": {"_id": "$order_date", "revenue": {"$sum": "$total_amount"}}}
          ])
    """
    start_time = time.time()
    
    try:
        result = mongo_client.execute_aggregation(collection, pipeline)
        execution_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "data": result,
            "count": len(result),
            "execution_time_ms": round(execution_time, 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2)
        }

@mcp.tool()
def mongodb_insert(
    collection: str,
    document: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> Dict[str, Any]:
    """
    Insert document(s) into MongoDB collection
    
    Args:
        collection: Collection name
        document: Single document dict or list of documents
        
    Examples:
        - Insert order: mongodb_insert("orders", {
            "customer_id": "CUST001", 
            "total_amount": 250.50,
            "order_date": "2024-12-13"
          })
    """
    start_time = time.time()
    
    try:
        result = mongo_client.execute_insert(collection, document)
        execution_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "data": result,
            "execution_time_ms": round(execution_time, 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2)
        }

@mcp.tool()
def mongodb_update(
    collection: str,
    filter_criteria: Dict[str, Any],
    update_data: Dict[str, Any],
    upsert: bool = False
) -> Dict[str, Any]:
    """
    Update documents in MongoDB collection
    
    Args:
        collection: Collection name
        filter_criteria: Match criteria for documents to update
        update_data: Update operations (use $set, $inc, etc.)
        upsert: Insert if no match found (default: False)
        
    Examples:
        - Update customer: mongodb_update("customers", 
            {"customer_id": "CUST001"},
            {"$set": {"total_spent": 1250.75}}
          )
    """
    start_time = time.time()
    
    try:
        result = mongo_client.execute_update(collection, filter_criteria, update_data, upsert)
        execution_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "data": result,
            "execution_time_ms": round(execution_time, 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2)
        }

@mcp.tool()
def mongodb_get_collections() -> Dict[str, Any]:
    """
    Get list of all collections in database
    
    Returns:
        List of collection names with document counts
        
    Examples:
        - Get all: mongodb_get_collections()
    """
    start_time = time.time()
    
    try:
        result = mongo_client.get_collections()
        execution_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "data": result,
            "execution_time_ms": round(execution_time, 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2)
        }

@mcp.tool()
def mongodb_describe_collection(
    collection: str,
    sample_size: int = 5
) -> Dict[str, Any]:
    """
    Get collection schema and sample documents
    
    Args:
        collection: Collection name
        sample_size: Number of sample documents (default: 5)
        
    Examples:
        - Describe orders: mongodb_describe_collection("orders", 3)
    """
    start_time = time.time()
    
    try:
        result = mongo_client.describe_collection(collection, sample_size)
        execution_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "data": result,
            "execution_time_ms": round(execution_time, 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2)
        }

# ========== BUSINESS ANALYTICS TOOLS ==========

@mcp.tool()
def get_revenue_analytics(
    time_period: str = "daily",
    days_back: int = 7
) -> Dict[str, Any]:
    """
    Get comprehensive revenue analytics
    
    Args:
        time_period: 'daily', 'weekly', or 'monthly'
        days_back: Number of days to look back
        
    Examples:
        - get_revenue_analytics("daily", 7)  # Last 7 days daily revenue
        - get_revenue_analytics("weekly", 30)  # Last 30 days by week
    """
    try:
        if time_period == "daily":
            pipeline = [
                {"$group": {
                    "_id": "$order_date",
                    "total_revenue": {"$sum": "$total_amount"},
                    "order_count": {"$sum": 1},
                    "avg_order_value": {"$avg": "$total_amount"}
                }},
                {"$sort": {"_id": -1}},
                {"$limit": days_back}
            ]
        elif time_period == "weekly":
            pipeline = [
                {"$group": {
                    "_id": {"$substr": ["$order_date", 0, 7]},  # YYYY-MM format for weekly grouping
                    "total_revenue": {"$sum": "$total_amount"},
                    "order_count": {"$sum": 1}
                }},
                {"$sort": {"_id": -1}},
                {"$limit": 8}
            ]
        else:  # monthly
            pipeline = [
                {"$group": {
                    "_id": {"$substr": ["$order_date", 0, 7]},  # YYYY-MM format
                    "total_revenue": {"$sum": "$total_amount"},
                    "order_count": {"$sum": 1}
                }},
                {"$sort": {"_id": -1}}
            ]
        
        result = mongo_client.execute_aggregation("orders", pipeline)
        return {"success": True, "data": result, "time_period": time_period}
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_customer_insights(analysis_type: str = "segments") -> Dict[str, Any]:
    """
    Get customer analytics and insights
    
    Args:
        analysis_type: 'segments', 'top_spenders', 'loyalty', or 'count'
        
    Examples:
        - get_customer_insights("segments")  # Customer segments breakdown
        - get_customer_insights("top_spenders")  # Top 10 customers by spend
        - get_customer_insights("count")  # Count customers by segment
    """
    try:
        if analysis_type == "segments":
            pipeline = [
                {"$group": {
                    "_id": "$segment",
                    "count": {"$sum": 1},
                    "avg_total_spent": {"$avg": "$total_spent"},
                    "max_spent": {"$max": "$total_spent"}
                }},
                {"$sort": {"count": -1}}
            ]
        elif analysis_type == "top_spenders":
            pipeline = [
                {"$sort": {"total_spent": -1}},
                {"$limit": 10},
                {"$project": {
                    "customer_id": 1,
                    "name": 1,
                    "total_spent": 1,
                    "segment": 1,
                    "order_count": 1
                }}
            ]
        elif analysis_type == "count":
            pipeline = [
                {"$group": {
                    "_id": "$segment",
                    "customer_count": {"$sum": 1}
                }},
                {"$sort": {"customer_count": -1}}
            ]
        else:  # loyalty
            pipeline = [
                {"$group": {
                    "_id": "$segment",
                    "avg_order_count": {"$avg": "$order_count"},
                    "avg_total_spent": {"$avg": "$total_spent"},
                    "customer_count": {"$sum": 1}
                }},
                {"$sort": {"avg_total_spent": -1}}
            ]
        
        result = mongo_client.execute_aggregation("customers", pipeline)
        return {"success": True, "data": result, "analysis_type": analysis_type}
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_menu_performance(metric: str = "popularity") -> Dict[str, Any]:
    """
    Analyze menu item performance
    
    Args:
        metric: 'popularity', 'revenue', or 'categories'
        
    Examples:
        - get_menu_performance("popularity")  # Most ordered items
        - get_menu_performance("revenue")  # Highest revenue items
        - get_menu_performance("categories")  # Performance by category
    """
    try:
        if metric == "popularity":
            pipeline = [
                {"$unwind": "$items"},
                {"$group": {
                    "_id": "$items.item_id",
                    "order_frequency": {"$sum": "$items.quantity"},
                    "revenue_generated": {"$sum": {"$multiply": ["$items.quantity", "$items.price"]}},
                    "times_ordered": {"$sum": 1}
                }},
                {"$sort": {"order_frequency": -1}},
                {"$limit": 10}
            ]
        elif metric == "revenue":
            pipeline = [
                {"$unwind": "$items"},
                {"$group": {
                    "_id": "$items.item_id",
                    "total_revenue": {"$sum": {"$multiply": ["$items.quantity", "$items.price"]}},
                    "quantity_sold": {"$sum": "$items.quantity"}
                }},
                {"$sort": {"total_revenue": -1}},
                {"$limit": 10}
            ]
        else:  # categories - simplified approach
            pipeline = [
                {"$group": {
                    "_id": "$category",
                    "item_count": {"$sum": 1},
                    "avg_price": {"$avg": "$price"},
                    "price_range": {
                        "$push": "$price"
                    }
                }},
                {"$sort": {"item_count": -1}}
            ]
        
        collection = "orders" if metric in ["popularity", "revenue"] else "menu_items"
        result = mongo_client.execute_aggregation(collection, pipeline)
        return {"success": True, "data": result, "metric": metric}
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_operational_metrics(metric_type: str = "order_status") -> Dict[str, Any]:
    """
    Get operational performance metrics
    
    Args:
        metric_type: 'order_status', 'order_types', 'peak_hours', or 'payment_methods'
        
    Examples:
        - get_operational_metrics("order_status")  # Order status breakdown
        - get_operational_metrics("order_types")  # Dine-in vs Delivery
        - get_operational_metrics("peak_hours")  # Busiest hours analysis
    """
    try:
        if metric_type == "order_status":
            pipeline = [
                {"$group": {
                    "_id": "$order_status",
                    "count": {"$sum": 1},
                    "total_value": {"$sum": "$total_amount"},
                    "avg_value": {"$avg": "$total_amount"}
                }},
                {"$sort": {"count": -1}}
            ]
        elif metric_type == "order_types":
            pipeline = [
                {"$group": {
                    "_id": "$order_type",
                    "count": {"$sum": 1},
                    "total_revenue": {"$sum": "$total_amount"},
                    "avg_order_value": {"$avg": "$total_amount"}
                }},
                {"$sort": {"total_revenue": -1}}
            ]
        elif metric_type == "payment_methods":
            pipeline = [
                {"$group": {
                    "_id": "$payment_mode",
                    "transaction_count": {"$sum": 1},
                    "total_amount": {"$sum": "$total_amount"}
                }},
                {"$sort": {"total_amount": -1}}
            ]
        else:  # peak_hours - simplified without date parsing
            pipeline = [
                {"$group": {
                    "_id": "$order_date",
                    "daily_orders": {"$sum": 1},
                    "daily_revenue": {"$sum": "$total_amount"}
                }},
                {"$sort": {"daily_orders": -1}},
                {"$limit": 10}
            ]
        
        result = mongo_client.execute_aggregation("orders", pipeline)
        return {"success": True, "data": result, "metric_type": metric_type}
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def quick_stats(collection: str = "orders") -> Dict[str, Any]:
    """
    Get quick statistics for any collection
    
    Args:
        collection: Collection name (orders, customers, menu_items, etc.)
        
    Examples:
        - quick_stats("orders")  # Order statistics
        - quick_stats("customers")  # Customer statistics  
        - quick_stats("menu_items")  # Menu statistics
    """
    try:
        if collection == "orders":
            pipeline = [
                {"$group": {
                    "_id": None,
                    "total_orders": {"$sum": 1},
                    "total_revenue": {"$sum": "$total_amount"},
                    "avg_order_value": {"$avg": "$total_amount"},
                    "max_order": {"$max": "$total_amount"},
                    "min_order": {"$min": "$total_amount"}
                }},
                {"$project": {"_id": 0}}
            ]
        elif collection == "customers":
            pipeline = [
                {"$group": {
                    "_id": None,
                    "total_customers": {"$sum": 1},
                    "avg_spent": {"$avg": "$total_spent"},
                    "max_spent": {"$max": "$total_spent"},
                    "avg_orders": {"$avg": "$order_count"}
                }},
                {"$project": {"_id": 0}}
            ]
        else:  # menu_items or others
            pipeline = [
                {"$group": {
                    "_id": None,
                    "total_items": {"$sum": 1},
                    "avg_price": {"$avg": "$price"},
                    "max_price": {"$max": "$price"},
                    "min_price": {"$min": "$price"}
                }},
                {"$project": {"_id": 0}}
            ]
        
        result = mongo_client.execute_aggregation(collection, pipeline)
        return {"success": True, "data": result, "collection": collection}
    
    except Exception as e:
        return {"error": str(e)}

def setup_server():
    """Setup and configure the MCP server"""
    
    # Test database connection on startup
    if not mongo_client.connect():
        logger.error("Failed to connect to MongoDB on startup")
        raise ConnectionError("MongoDB connection failed")
    
    logger.info(f"Connected to MongoDB database: {mongo_client.db_name}")
    logger.info("All tools registered via decorators")
    
    return mcp

def main():
    """Main server entry point"""
    try:
        server_instance = setup_server()
        
        # Log available collections
        collections = mongo_client.list_collections()
        logger.info(f"Available collections: {collections}")
        
        logger.info("MongoDB Hotel Analytics MCP Server starting on HTTP...")
        logger.info("Server will be available at: http://localhost:8000")
        
        # Run the server with HTTP transport
        server_instance.run(transport="http", host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        mongo_client.disconnect()
        logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        mongo_client.disconnect()
        raise

if __name__ == "__main__":
    main()