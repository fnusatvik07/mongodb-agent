"""
Get MongoDB collections tool
"""

from typing import Dict, Any, List
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def mongodb_get_collections() -> List[Dict[str, Any]]:
        """Get list of all collections in database

        Returns:
            List of collection names with document counts
            
        Examples:
            - Get all: mongodb_get_collections()
        """
        try:
            collections = []
            for collection_name in db.list_collection_names():
                count = db[collection_name].count_documents({})
                collections.append({
                    "name": collection_name,
                    "document_count": count
                })
            return collections
        except Exception as e:
            return {"error": f"Failed to get collections: {str(e)}"}