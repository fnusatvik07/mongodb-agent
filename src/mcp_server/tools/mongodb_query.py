"""
MongoDB query tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def mongodb_query(collection: str, query: Dict[str, Any] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Execute a MongoDB find query

        Args:
            collection: Collection name
            query: Query filter (default: {} for all)
            limit: Max documents to return
            
        Examples:
            - mongodb_query("orders")
            - mongodb_query("customers", {"segment": "vip"})
        """
        try:
            if query is None:
                query = {}
            
            cursor = db[collection].find(query).limit(limit)
            results = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
                results.append(doc)
            return results
        except Exception as e:
            return {"error": f"Query failed: {str(e)}"}