from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from database import UserProfile, ProfileDB
from tools import fetch_cyber_news  # Imports our clean native function

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
        # 1. Sync background profile interest maps
        self.sync_memory(user_id, query, style_desc)
        
        # 2. Call the clean, native Python data utility directly (guaranteed to be a list object)
        articles_data = fetch_cyber_news(query)
        
        # Strict validation fallback to protect the LangChain invoke method downstream
        if not isinstance(articles_data, list):
            return [{"title": "System Diagnostic Failure", "source": "Engine Core", "summary": "Data stream failed list array integrity validation requirements.", "url": "#"}]

        system_prompt = (
            "You are a world-class Threat Intelligence Director compiling an elite intelligence briefing dashboard.\n\n"
            f"ROLE-BASED DESIGN CONSTRAINT: {style_desc}\n\n"
            "CRITICAL EXECUTABLE RULES:\n"
            "1. Read the provided article context carefully.\n"
            "2. Synthesize a concise, high-impact overview explaining exactly what happened, and add a specific 'Impact/Action Item' customized to the requested role.\n"
            "3. Do not include introductory text, numbers, markdown headings, or references to other articles. Output the synthesized text only."
        )

        briefing_deck = []
        
        # 3. Step across each dictionary packet securely
        for art in articles_data:
            synthesis_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", f"Source Article Headline: {art.get('title', 'Alert')}\nContext: {art.get('description', 'Empty context data.')}")
            ])
            
            try:
                ai_summary = self.model.invoke(synthesis_prompt).content
            except Exception as e:
                ai_summary = f"Failed to synthesize this specific article container record: {str(e)}"
            
            briefing_deck.append({
                "title": art.get("title", "No Title Available"),
                "source": art.get("source", "Unknown Source"),
                "summary": ai_summary,
                "url": art.get("url", "#")
            })
            
        return briefing_deck
