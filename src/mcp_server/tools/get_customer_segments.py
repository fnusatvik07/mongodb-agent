"""
Customer segments analytics tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def get_customer_segments_breakdown() -> List[Dict[str, Any]]:
        """Get breakdown of customer segments with spending statistics

        Returns:
            List of segments with customer count and spending metrics
        """
        try:
            pipeline = [
                {"$group": {
                    "_id": "$segment",
                    "customer_count": {"$sum": 1},
                    "total_spending": {"$sum": "$total_spent"},
                    "avg_spending": {"$avg": "$total_spent"},
                    "max_spending": {"$max": "$total_spent"},
                    "min_spending": {"$min": "$total_spent"},
                    "avg_loyalty_points": {"$avg": "$loyalty_points"}
                }},
                {"$sort": {"total_spending": -1}}
            ]
            return list(db["customers"].aggregate(pipeline))
        except Exception as e:
            return {"error": f"Customer segments analysis failed: {str(e)}"}