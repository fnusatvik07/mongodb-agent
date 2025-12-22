"""
Operational metrics tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def get_payment_methods_breakdown() -> List[Dict[str, Any]]:
        """Get breakdown of orders by payment method

        Returns:
            List of payment methods with order counts and revenue totals
        """
        try:
            pipeline = [
                {"$group": {
                    "_id": "$payment_method",
                    "order_count": {"$sum": 1},
                    "total_revenue": {"$sum": "$total_amount"},
                    "avg_order_value": {"$avg": "$total_amount"}
                }},
                {"$sort": {"order_count": -1}}
            ]
            return list(db["orders"].aggregate(pipeline))
        except Exception as e:
            return {"error": f"Payment methods breakdown failed: {str(e)}"}