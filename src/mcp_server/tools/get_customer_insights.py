"""
Customer insights tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def get_top_customers_by_spending(limit: int = 10) -> List[Dict[str, Any]]:
        """Get top customers ranked by total spending

        Args:
            limit: Number of top customers to return (default: 10)
            
        Returns:
            List of customers with their spending details
        """
        try:
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
            return {"error": f"Customer insights failed: {str(e)}"}