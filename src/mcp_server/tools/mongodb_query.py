"""MongoDB query tool for finding documents in collections."""

from typing import Dict, Any, List
from mcp_server.utils.db_client import mongo_client
from mcp_server.mcp_instance import mcp

@mcp.tool()
def mongodb_query(
        collection: str, 
        query: Dict[str, Any] = None, 
        limit: int = 10
    ) -> Dict[str, Any]:
        """Execute a MongoDB find query on the specified collection.

        Args:
            collection: Collection name (orders, customers, menu_items, users, audit_logs, delivery_details)
            query: MongoDB query filter dictionary (default: {} for all documents)
            limit: Maximum number of documents to return (default: 10 for previews, increase when asked)
            
        Returns:
            Dict with success status, data array, and count
            
        Key Patterns:
            Basic: {"field": "value"}
            Comparison: {"amount": {"$gte": 50}}
            Multiple conditions: {"status": "pending", "total_amount": {"$gte": 20}}
            OR logic: {"$or": [{"status": "pending"}, {"status": "processing"}]}
            Arrays: {"items.name": "Pizza"}
            
        WORKFLOW:
            1. ALWAYS use mongodb_get_collections() first to see available collections
            2. ALWAYS use mongodb_describe_collection() to discover exact field names and structure
            3. Then construct queries using actual field names from schema
            
        Use standard MongoDB operators ($gt, $lt, $gte, $lte, $in, $ne, $or, $and).
        Always pass a structured MongoDB query dictionary. Do not pass natural language text in query.
        """
        try:
            if not collection or not isinstance(collection, str):
                return {"success": False, "error": "Collection name must be a non-empty string"}
                
            if query is None:
                query = {}
            elif not isinstance(query, dict):
                return {"success": False, "error": "Query must be a dictionary"}
                
            if not isinstance(limit, int) or limit <= 0:
                return {"success": False, "error": "Limit must be a positive integer"}
                
            db = mongo_client.db
            cursor = db[collection].find(query).limit(limit)
            results = []
            for doc in cursor:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
                results.append(doc)
                
            return {
                "success": True,
                "data": results,
                "count": len(results)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Query operation failed: {str(e)}"
            }