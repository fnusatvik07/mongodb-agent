"""
Order status breakdown tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def get_order_status_breakdown() -> List[Dict[str, Any]]:
        """Get breakdown of orders by status

        Returns:
            List of order statuses with counts and revenue totals
        """
        try:
            pipeline = [
                {"$group": {
                    "_id": "$status",
                    "order_count": {"$sum": 1},
                    "total_revenue": {"$sum": "$total_amount"},
                    "avg_order_value": {"$avg": "$total_amount"}
                }},
                {"$sort": {"order_count": -1}}
            ]
            return list(db["orders"].aggregate(pipeline))
        except Exception as e:
            return {"error": f"Order status breakdown failed: {str(e)}"}