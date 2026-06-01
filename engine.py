from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from database import UserProfile, ProfileDB
from tools import fetch_cyber_news

class AgentOrchestrator:
    def __init__(self):
        self.model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
        self.db = ProfileDB()

    def sync_memory(self, user_id: str, query: str, style_desc: str) -> UserProfile:
        profile = self.db.get_user(user_id)
        updater_prompt = ChatPromptTemplate.from_messages([
            ("system", "Analyze the briefing request. Update the JSON user profile tracking history. Append core keywords to tracking history."),
            ("user", "Profile: {profile}\nCuration Focus: {query}\nStyle Requirements: {style}")
        ])
        structured_model = self.model.with_structured_output(UserProfile, method="function_calling")
        try:
            updated = (updater_prompt | structured_model).invoke({
                "profile": profile.model_dump_json(), "query": query, "style": style_desc
            })
            self.db.save_user(updated)
            return updated
        except Exception:
            return profile

    def run(self, user_id: str, query: str, style_desc: str) -> list:
        # 1. Update background user preference matrices
        self.sync_memory(user_id, query, style_desc)
        
        # FIX: Swapping .invoke() out for .run() lets the dict array pass through cleanly
        # without LangChain forcing string serialization structures on it.
        articles_data = fetch_cyber_news.run({"query": query})
        
        # Defensive fallback if the tool output hits formatting anomalies
        if isinstance(articles_data, str):
            return [{"title": "Data Format Alert", "source": "System Core", "summary": "The data stream required string serialization fallback. Please rerun the dashboard request.", "url": "#"}]

        system_prompt = (
            "You are a world-class Threat Intelligence Director compiling an elite intelligence briefing dashboard.\n\n"
            f"ROLE-BASED DESIGN CONSTRAINT: {style_desc}\n\n"
            "CRITICAL EXECUTABLE RULES:\n"
            "1. Read the provided article context carefully.\n"
            "2. Synthesize a concise, high-impact overview explaining exactly what happened, and add a specific 'Impact/Action Item' customized to the requested role.\n"
            "3. Do not include introductory text, numbers, markdown headings, or references to other articles. Output the synthesized text only."
        )

        briefing_deck = []
        
        # 3. Step across each dict data object safely
        for art in articles_data:
            synthesis_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", f"Source Article Headline: {art['title']}\nContext: {art['description']}")
            ])
            
            ai_summary = self.model.invoke(synthesis_prompt).content
            
            briefing_deck.append({
                "title": art["title"],
                "source": art["source"],
                "summary": ai_summary,
                "url": art["url"]
            })
            
        return briefing_deck
