import os
import requests
import json
from langchain_core.tools import tool

@tool
def fetch_cyber_news(query: str) -> str:
    """Queries the live web for the latest cybersecurity, privacy, and data governance news articles and returns structured data."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return json.dumps({"error": "Missing NEWS_API_KEY environment variable."})
    
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
            return json.dumps({"error": data.get('message', 'Unknown API Error')})
            
        articles = data.get("articles", [])
        if not articles:
            return json.dumps({"error": f"No high-relevancy updates found for target: '{query}'."})
            
        # Compile structured metadata tracking packets
        payload_list = []
        for art in articles:
            payload_list.append({
                "title": art.get("title", "No Title Available"),
                "description": art.get("description", "No Context Snippet Available"),
                "source": art.get("source", {}).get("name", "Unknown Source"),
                "url": art.get("url", "#")
            })
            
        return json.dumps(payload_list)
        
    except Exception as e:
        return json.dumps({"error": str(e)})
