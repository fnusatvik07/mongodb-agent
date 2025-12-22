"""
MongoDB Hotel Analytics MCP Server
Main server implementation using FastMCP with modular tools
"""

import logging
import os
import sys
from fastmcp import FastMCP

# Set matplotlib backend for headless server environment
import matplotlib
matplotlib.use('Agg')

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
from tools import get_customer_segments
from tools import get_menu_performance
from tools import get_menu_revenue
from tools import get_operational_metrics
from tools import get_order_status
from tools import get_order_types
from tools import get_revenue_by_date
from tools import search_orders
from tools import quick_stats
from tools import generate_chart
from tools import get_data_range

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("mongodb-hotel-analytics")

def setup_server():
    """Setup and configure the MCP server"""
    
    # Test database connection on startup
    if not mongo_client.connect():
        logger.error("Failed to connect to MongoDB on startup")
        raise ConnectionError("MongoDB connection failed")
    
    logger.info(f"Connected to MongoDB database: {mongo_client.db_name}")
    
    # Register all tools
    mongodb_query.register_tool(mcp, mongo_client.db)
    mongodb_aggregate.register_tool(mcp, mongo_client.db)
    mongodb_insert.register_tool(mcp, mongo_client.db)
    mongodb_update.register_tool(mcp, mongo_client.db)
    mongodb_get_collections.register_tool(mcp, mongo_client.db)
    mongodb_describe_collection.register_tool(mcp, mongo_client.db)
    get_revenue_analytics.register_tool(mcp, mongo_client.db)
    get_customer_insights.register_tool(mcp, mongo_client.db)
    get_customer_segments.register_tool(mcp, mongo_client.db)
    get_menu_performance.register_tool(mcp, mongo_client.db)
    get_menu_revenue.register_tool(mcp, mongo_client.db)
    get_operational_metrics.register_tool(mcp, mongo_client.db)
    get_order_status.register_tool(mcp, mongo_client.db)
    get_order_types.register_tool(mcp, mongo_client.db)
    get_revenue_by_date.register_tool(mcp, mongo_client.db)
    search_orders.register_tool(mcp, mongo_client.db)
    quick_stats.register_tool(mcp, mongo_client.db)
    generate_chart.register_tool(mcp, mongo_client.db)
    get_data_range.register_tool(mcp, mongo_client.db)
    
    logger.info("All tools registered successfully")
    
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
        logger.error(f"Server error: {e}")
        mongo_client.disconnect()

if __name__ == "__main__":
    main()