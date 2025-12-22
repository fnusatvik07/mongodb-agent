"""
MongoDB aggregate tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def mongodb_aggregate(collection: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute MongoDB aggregation pipeline

        Args:
            collection: Collection name
            pipeline: List of aggregation stages
            
        Examples:
            - Daily revenue: mongodb_aggregate("orders", [
                {"$group": {"_id": "$order_date", "revenue": {"$sum": "$total_amount"}}}
              ])
        """
        try:
            cursor = db[collection].aggregate(pipeline)
            results = []
            for doc in cursor:
                # Convert ObjectId to string if present
                if '_id' in doc and hasattr(doc['_id'], '__str__'):
                    doc['_id'] = str(doc['_id'])
                results.append(doc)
            return results
        except Exception as e:
            return {"error": f"Aggregation failed: {str(e)}"}