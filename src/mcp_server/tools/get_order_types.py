"""
Order types breakdown tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def get_order_types_breakdown() -> List[Dict[str, Any]]:
        """Get breakdown of orders by type (dine-in, delivery, etc.)

        Returns:
            List of order types with counts, revenue and averages
        """
        try:
            pipeline = [
                {"$group": {
                    "_id": "$order_type",
                    "order_count": {"$sum": 1},
                    "total_revenue": {"$sum": "$total_amount"},
                    "avg_order_value": {"$avg": "$total_amount"},
                    "min_order_value": {"$min": "$total_amount"},
                    "max_order_value": {"$max": "$total_amount"}
                }},
                {"$sort": {"total_revenue": -1}}
            ]
            return list(db["orders"].aggregate(pipeline))
        except Exception as e:
            return {"error": f"Order types breakdown failed: {str(e)}"}