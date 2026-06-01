from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from database import UserProfile, ProfileDB
from tools import fetch_cyber_news

class AgentOrchestrator:
    def __init__(self):
        self.model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1) # Lower temp for high-accuracy analysis
        self.db = ProfileDB()

    def sync_memory(self, user_id: str, current_query: str, current_style: str) -> UserProfile:
        profile = self.db.get_user(user_id)
        
        updater_prompt = ChatPromptTemplate.from_messages([
            ("system", "Analyze the briefing request. Update the JSON user profile tracking history. Append core keywords to tracking history."),
            ("user", "Profile: {profile}\nCuration Focus: {query}\nStyle Requirements: {style}")
        ])
        
        structured_model = self.model.with_structured_output(UserProfile, method="function_calling")
        
        try:
            updated = (updater_prompt | structured_model).invoke({
                "profile": profile.model_dump_json(), "query": current_query, "style": current_style
            })
            self.db.save_user(updated)
            return updated
        except Exception:
            return profile

    def run(self, user_id: str, query: str, style_desc: str) -> str:
        # Update user profile tracking state in the background
        self.sync_memory(user_id, query, style_desc)
        
        # Pull live global threat/vulnerability datasets based on hidden query matrices
        raw_news_payload = fetch_cyber_news.invoke({"query": query})
        
        system_prompt = (
            "You are a world-class Threat Intelligence Director compiling an elite morning briefing newsletter.\n\n"
            "Your job is to read the raw industry news feed provided, pick out the most critical items, and format a strict 'Top 5 Things to Know' briefing.\n\n"
            f"ROLE-BASED DESIGN CONSTRAINT: {style_desc}\n\n"
            "CRITICAL FORMAT RULES:\n"
            "1. Output EXACTLY 5 clear, separated items.\n"
            "2. Ensure each item contains a bold title, a clear explanation of what happened, and a direct 'Impact/Action Item' statement tailored to the user's operational role.\n"
            "3. Do not include conversational prefaces or closing pleasantries (e.g., 'Here is your briefing'). Start directly with item 1."
        )
        
        synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Analyze and synthesize these raw data points into the Top 5 layout:\n\n{payload}")
        ])
        
        return (synthesis_prompt | self.model).invoke({"payload": raw_news_payload}).content
