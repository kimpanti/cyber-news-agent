import requests
from langchain_core.tools import tool
import os

@tool
def fetch_cyber_news(query: str) -> str:
    """Fetches live cyber security, privacy, and AI governance articles."""
    news_api_key = os.getenv("NEWS_API_KEY")
    niche_filter = ' (cybersecurity OR privacy OR "AI safety" OR "data breach")'
    full_query = f"{query}{niche_filter}"

    url = f"https://newsapi.org/v2/everything?q={requests.utils.quote(full_query)}&sortBy=publishedAt&language=en&pageSize=4&apiKey={news_api_key}"

    try:
        res = requests.get(url).json()
        articles = res.get("articles", [])
        if not articles:
            return "No fresh industry insights found matching that criteria."

        output = []
        for art in articles:
            output.append(f"Title: {art['title']}\nSource: {art['source']['name']}\nSummary: {art['description']}\n---")
        return "\n".join(output)
    except Exception as e:
        return f"Retrieval optimization failed: {str(e)}"
