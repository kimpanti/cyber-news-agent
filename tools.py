import os
import requests

def fetch_cyber_news(topic_query: str) -> list:
    """Queries the live web for premium Australian tech, data, and security news."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return [{"title": "Configuration Error", "source": "System Core", "description": "Missing NEWS_API_KEY in Streamlit Secrets.", "url": "#"}]
    
    # Geographic and domain anchoring matrices for Australia
    # We mix top tier domestic sources with major global tech wires to capture international events hitting AU
    premium_domains = (
        "itnews.com.au,cyberdaily.com.au,abc.net.au,afr.com,theage.com.au,"
        "smh.com.au,theregister.com,bleepingcomputer.com,techcrunch.com,zdnet.com"
    )
    
    # Force the query to have a strict Australian hook or impact footprint
    localized_query = f"({topic_query}) AND (Australia OR Australian OR AUD OR OAIC)"
    
    url = (
        f"https://newsapi.org/v2/everything?q={localized_query}"
        f"&domains={premium_domains}"
        f"&sortBy=relevancy"
        f"&language=en"
        f"&pageSize=5"
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get("status") != "ok":
            return [{"title": "API Warning", "source": "NewsAPI Wire", "description": data.get('message', 'Regional query limit anomaly.'), "url": "#"}]
            
        articles = data.get("articles", [])
        if not articles:
            return [{"title": "No Direct National Briefings Located", "source": "Australian Search Index", "description": f"No high-relevancy premium updates matched this localized matrix: '{topic_query}' within Australia recently.", "url": "#"}]
            
        payload_list = []
        for art in articles:
            payload_list.append({
                "title": art.get("title", "No Headline Available"),
                "description": art.get("description", "No Context Snippet Available"),
                "source": art.get("source", {}).get("name", "Premium Wire"),
                "url": art.get("url", "#")
            })
        return payload_list
        
    except Exception as e:
        return [{"title": "Network Error", "source": "System Transceiver", "description": str(e), "url": "#"}]
