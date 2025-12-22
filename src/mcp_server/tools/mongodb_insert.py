"""
MongoDB insert tool
"""

from typing import Dict, Any, List, Union
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def mongodb_insert(collection: str, document: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Insert document(s) into MongoDB collection

        Args:
            collection: Collection name
            document: Single document dict or list of documents
            
        Examples:
            - Insert order: mongodb_insert("orders", {
                "customer_id": "CUST001", 
                "total_amount": 250.50,
                "order_date": "2024-12-13"
              })
        """
        try:
            if isinstance(document, list):
                result = db[collection].insert_many(document)
                return {
                    "inserted_count": len(result.inserted_ids),
                    "inserted_ids": [str(id) for id in result.inserted_ids]
                }
            else:
                result = db[collection].insert_one(document)
                return {
                    "inserted_count": 1,
                    "inserted_id": str(result.inserted_id)
                }
        except Exception as e:
            return {"error": f"Insert failed: {str(e)}"}