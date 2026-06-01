import os
import requests
from langchain_core.tools import tool

@tool
def fetch_cyber_news(query: str) -> list:
    """Queries the live web for the latest cybersecurity, privacy, and data governance news articles and returns a structured list."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return [{"title": "Authentication Error", "source": "System Core", "description": "Missing NEWS_API_KEY environment variable.", "url": "#"}]
    
    refined_query = f"({query}) AND (cybersecurity OR privacy OR 'data breach' OR vulnerability)"
    
    url = (
        f"https://newsapi.org/v2/everything?q={refined_query}"
        f"&searchIn=title,description"
        f"&sortBy=relevancy"
        f"&language=en"
        f"&pageSize=5"
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get("status") != "ok":
            return [{"title": "API Operational Warning", "source": "NewsAPI Portal", "description": data.get('message', 'Unknown API Error'), "url": "#"}]
            
        articles = data.get("articles", [])
        if not articles:
            return [{"title": "Zero Hits Returned", "source": "Search Index", "description": f"No high-relevancy updates found for target: '{query}'.", "url": "#"}]
            
        payload_list = []
        for art in articles:
            payload_list.append({
                "title": art.get("title", "No Title Available"),
                "description": art.get("description", "No Context Snippet Available"),
                "source": art.get("source", {}).get("name", "Unknown Source"),
                "url": art.get("url", "#")
            })
            
        return payload_list
        
    except Exception as e:
        return [{"title": "Network Exception Connection Failed", "source": "System Network Transceiver", "description": str(e), "url": "#"}]
