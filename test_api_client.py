"""
Simple test client for FastAPI endpoints
Test the MongoDB Analytics Agent API functionality
"""

import requests
import json
from typing import Dict, Any

class AnalyticsAPIClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_tools(self) -> Dict[str, Any]:
        """Get available tools"""
        try:
            response = requests.get(f"{self.base_url}/tools")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def query(self, query: str, generate_chart: bool = False, chart_type: str = "auto") -> Dict[str, Any]:
        """Send analytics query"""
        try:
            payload = {
                "query": query,
                "generate_chart": generate_chart,
                "chart_type": chart_type
            }
            response = requests.post(
                f"{self.base_url}/query",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_charts(self) -> Dict[str, Any]:
        """List available charts"""
        try:
            response = requests.get(f"{self.base_url}/charts")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def clear_charts(self) -> Dict[str, Any]:
        """Clear all charts"""
        try:
            response = requests.delete(f"{self.base_url}/clear-charts")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def test_api():
    """Test the API endpoints"""
    client = AnalyticsAPIClient()
    
    print("🧪 Testing MongoDB Analytics Agent API")
    print("=" * 50)
    
    # Test health check
    print("\n1. Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    # Test tools list
    print("\n2. Available Tools:")
    tools = client.get_tools()
    if "tools" in tools:
        print(f"Found {tools['total_count']} tools:")
        for tool in tools["tools"][:3]:  # Show first 3
            print(f"   • {tool['name']}: {tool['description'][:50]}...")
    else:
        print(json.dumps(tools, indent=2))
    
    # Test simple query
    print("\n3. Simple Query:")
    result = client.query("Show me all available collections")
    if "success" in result:
        print(f"Success: {result['success']}")
        print(f"Response: {result['response'][:100]}...")
        print(f"Tools used: {result.get('tools_used', [])}")
    else:
        print(json.dumps(result, indent=2))
    
    # Test query with chart
    print("\n4. Query with Chart:")
    result = client.query("Show revenue by order type", generate_chart=True, chart_type="pie")
    if "success" in result:
        print(f"Success: {result['success']}")
        print(f"Chart generated: {result.get('chart_path')}")
        print(f"Chart title: {result.get('chart_title')}")
    else:
        print(json.dumps(result, indent=2))
    
    # List charts
    print("\n5. Available Charts:")
    charts = client.list_charts()
    if "charts" in charts:
        print(f"Found {charts['count']} charts")
        for chart in charts["charts"][:2]:
            print(f"   • {chart['filename']} ({chart['size']} bytes)")
    else:
        print(json.dumps(charts, indent=2))

if __name__ == "__main__":
    test_api()