import os
import requests
from langchain_core.tools import tool

@tool
def fetch_cyber_news(query: str) -> str:
    """Queries the live web for the latest cybersecurity, privacy, and data governance news articles."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return "Error: Missing NEWS_API_KEY environment variable."
    
    # We restrict the keywords programmatically to lock focus onto security/privacy domains
    refined_query = f"({query}) AND (cybersecurity OR privacy OR 'AI governance' OR breach)"
    
    url = f"https://newsapi.org/v2/everything?q={refined_query}&sortBy=publishedAt&pageSize=5"
    
    # FIX: Adding browser headers tricks NewsAPI into treating the cloud server like a local machine
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get("status") != "ok":
            return f"Failed to fetch news feed: {data.get('message', 'Unknown API Error')}"
            
        articles = data.get("articles", [])
        if not articles:
            return f"No active news updates located matching the industry query target: '{query}'."
            
        # Parse down the raw metadata feed into a clean string layout for the LLM
        payload_summary = []
        for idx, art in enumerate(articles, 1):
            title = art.get("title", "No Title Available")
            desc = art.get("description", "No Context Snippet Available")
            source = art.get("source", {}).get("name", "Unknown Source")
            payload_summary.append(f"[{idx}] {title}\nSource: {source}\nContext: {desc}\n")
            
        return "\n---\n".join(payload_summary)
        
    except Exception as e:
        return f"An operational exception occurred during network retrieval: {str(e)}"
