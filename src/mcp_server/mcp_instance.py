"""
FastMCP instance - shared across all modules to avoid circular imports
"""

from fastmcp import FastMCP

# Initialize FastMCP server instance
mcp = FastMCP("mongodb-hotel-analytics")