"""
Describe MongoDB collection tool
"""

from typing import Dict, Any
from fastmcp import FastMCP


def register_tool(mcp: FastMCP, db):
    @mcp.tool()
    def mongodb_describe_collection(collection: str, sample_size: int = 5) -> Dict[str, Any]:
        """Get collection schema and sample documents

        Args:
            collection: Collection name
            sample_size: Number of sample documents (default: 5)
            
        Examples:
            - Describe orders: mongodb_describe_collection("orders", 3)
        """
        try:
            # Get sample documents
            cursor = db[collection].find().limit(sample_size)
            samples = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                samples.append(doc)
            
            # Get collection stats
            count = db[collection].count_documents({})
            
            # Extract field names from samples
            fields = set()
            for doc in samples:
                fields.update(doc.keys())
            
            return {
                "collection": collection,
                "document_count": count,
                "fields": list(fields),
                "sample_documents": samples
            }
        except Exception as e:
            return {"error": f"Failed to describe collection: {str(e)}"}