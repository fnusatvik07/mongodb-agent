"""
Menu performance tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def get_top_menu_items_by_orders(limit: int = 10) -> List[Dict[str, Any]]:
        """Get most frequently ordered menu items

        Args:
            limit: Number of top items to return (default: 10)
            
        Returns:
            List of menu items with order frequency and revenue
        """
        try:
            pipeline = [
                {"$unwind": "$items"},
                {"$group": {
                    "_id": "$items.name",
                    "total_orders": {"$sum": "$items.quantity"},
                    "total_revenue": {"$sum": {"$multiply": ["$items.quantity", "$items.price"]}},
                    "avg_price": {"$avg": "$items.price"}
                }},
                {"$sort": {"total_orders": -1}},
                {"$limit": limit}
            ]
            return list(db["orders"].aggregate(pipeline))
        except Exception as e:
            return {"error": f"Menu performance analysis failed: {str(e)}"}