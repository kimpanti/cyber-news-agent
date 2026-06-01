from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq  # Swapped from langchain_openai
from database import UserProfile, ProfileDB
from tools import fetch_cyber_news
import os

class AgentOrchestrator:
    def __init__(self):
        # We use Llama 3 on Groq which is completely free and supports structured outputs
        self.model = ChatGroq(model="llama3-8b-8192", temperature=0.2)
        self.db = ProfileDB()

    def sync_memory(self, user_id: str, current_query: str, current_style: str) -> UserProfile:
        profile = self.db.get_user(user_id)
        
        updater_prompt = ChatPromptTemplate.from_messages([
            ("system", "Analyze the user's request. Return an updated JSON profile matching the schema precisely. Append new keywords to core_interests (max 8). Increment category_weights based on context."),
            ("user", "Profile: {profile}\nQuery: {query}\nSelected Style: {style}")
        ])
        
        structured_model = self.model.with_structured_output(UserProfile)
        updated = (updater_prompt | structured_model).invoke({
            "profile": profile.model_dump_json(), "query": current_query, "style": current_style
        })
        self.db.save_user(updated)
        return updated

    def run(self, user_id: str, query: str, style_desc: str) -> str:
        self.sync_memory(user_id, query, style_desc)
        raw_news_payload = fetch_cyber_news.invoke({"query": query})
        
        system_prompt = (
            "You are an industry-leading Cyber and AI intelligence agent.\n\n"
            f"STRICT OUTPUT STYLE CONSTRAINT: You must explain the news articles exactly like: {style_desc}. "
            "Do not break this character under any circumstances. Keep explanations highly engaging and accurate."
        )
        
        synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Synthesize this raw industry data payload into your style baseline:\n\n{payload}")
        ])
        
        return (synthesis_prompt | self.model).invoke({"payload": raw_news_payload}).content
