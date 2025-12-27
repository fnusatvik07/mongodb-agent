"""
Customer insights tool
"""

from typing import Dict, Any, List
from mcp_server.utils.db_client import mongo_client
from mcp_server.mcp_instance import mcp

@mcp.tool()
def get_top_customers_by_spending(limit: int = 10) -> List[Dict[str, Any]]:
        """Get top customers ranked by total spending.

        Args:
            limit: Number of top customers to return (default: 10)
            
        Returns:
            List of customers with spending details and customer information
            
        Provides customer rankings based on total_spent field.
        
        WORKFLOW:
            For custom customer analysis, first use:
            1. mongodb_get_collections() - to see available collections
            2. mongodb_describe_collection() - to understand field names and structure
        """
        try:
            db = mongo_client.db
            pipeline = [
                {"$sort": {"total_spent": -1}},
                {"$limit": limit},
                {"$project": {
                    "customer_id": 1,
                    "name": 1,
                    "segment": 1,
                    "total_spent": 1,
                    "loyalty_points": 1,
                    "email": 1
                }}
            ]
            return list(db["customers"].aggregate(pipeline))
        except Exception as e:
            return [{"error": f"Customer insights failed: {str(e)}"}]