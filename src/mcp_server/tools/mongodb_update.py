"""
MongoDB update tool
"""

from typing import Dict, Any
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def mongodb_update(collection: str, filter_criteria: Dict[str, Any], 
                      update_data: Dict[str, Any], upsert: bool = False) -> Dict[str, Any]:
        """Update documents in MongoDB collection

        Args:
            collection: Collection name
            filter_criteria: Match criteria for documents to update
            update_data: Update operations (use $set, $inc, etc.)
            upsert: Insert if no match found (default: False)
            
        Examples:
            - Update customer: mongodb_update("customers", 
                {"customer_id": "CUST001"},
                {"$set": {"total_spent": 1250.75}}
              )
        """
        try:
            result = db[collection].update_many(filter_criteria, update_data, upsert=upsert)
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_id": str(result.upserted_id) if result.upserted_id else None
            }
        except Exception as e:
            return {"error": f"Update failed: {str(e)}"}