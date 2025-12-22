"""
Revenue analytics tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP
from datetime import datetime, timedelta


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def get_daily_revenue(start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get daily revenue breakdown for date range

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of daily revenue totals with order counts
        """
        try:
            # Parse dates and convert to match database format
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
            
            pipeline = [
                {"$match": {
                    "created_at": {
                        "$gte": start_dt.strftime("%Y-%m-%dT00:00:00Z"),
                        "$lte": end_dt.strftime("%Y-%m-%dT23:59:59Z")
                    }
                }},
                {"$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": {"$dateFromString": {"dateString": "$created_at"}}}},
                    "total_revenue": {"$sum": "$total_amount"},
                    "order_count": {"$sum": 1},
                    "avg_order_value": {"$avg": "$total_amount"}
                }},
                {"$sort": {"_id": 1}}
            ]
            
            results = list(db["orders"].aggregate(pipeline))
            
            if not results:
                # If no results, check what dates actually exist
                sample = db["orders"].find_one({}, {"created_at": 1})
                if sample:
                    return {"error": f"No orders found between {start_date} and {end_date}. Sample date in DB: {sample.get('created_at', 'No date found')}"}
                else:
                    return {"error": "No orders found in database"}
            
            return results
        except Exception as e:
            return {"error": f"Revenue analytics failed: {str(e)}"}