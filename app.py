import streamlit as st
from engine import AgentOrchestrator
from database import ProfileDB

st.set_page_config(page_title="Cyber Intelligence Briefing Engine", page_icon="🔒", layout="wide")

st.title("🔒 Cyber, Privacy & AI Security Briefing Engine")
st.caption("Automated threat intelligence and regulatory curation engine powered by LangChain & Groq")

# Detailed persona and internal routing profiles
PERSONAS = {
    "👔 Chief Information Security Officer (CISO)": {
        "desc": "A high-level executive briefing focused on systemic threat trends, material financial risk, vendor vulnerabilities, and business continuity metrics. Strict bullet points.",
        "keywords": "ransomware OR 'zero-day' OR breach OR supply-chain OR 'cyber insurance'"
    },
    "💻 Lead Security Engineer": {
        "desc": "A deep technical brief focused on exact exploit mechanics, CVE updates, architectural indicators of compromise (IOCs), and technical defensive mitigations.",
        "keywords": "exploit OR CVE OR vulnerability OR 'remote code execution' OR patch"
    },
    "⚖️ Privacy & Compliance Director": {
        "desc": "A governance briefing focusing heavily on regulatory enforcement actions, class-action privacy lawsuits, international framework violations (GDPR, CCPA, OAIC), and data handling compliance penalties.",
        "keywords": "GDPR OR fine OR compliance OR lawsuit OR 'data privacy' OR regulation"
    },
    "🤖 AI Safety & Governance Officer": {
        "desc": "A forward-looking assessment on AI vulnerabilities, shadow AI deployments, LLM data poisoning, model exfiltration risk, and emerging AI safety legal frameworks.",
        "keywords": "'shadow AI' OR 'LLM vulnerability' OR 'AI regulation' OR NIST-AIMF OR deepfake"
    }
}

user_id = "portfolio_user_demo"
orchestrator = AgentOrchestrator()
db = ProfileDB()

# LAYOUT: Two clear columns for enterprise tracking
col_sidebar, col_main = st.columns([1, 3])

with col_sidebar:
    st.subheader("📋 Executive Persona Selected")
    selected_role = st.selectbox("Select Your Profile Role:", list(PERSONAS.keys()))
    
    st.markdown("---")
    st.subheader("Persistent Profile State")
    if st.button("Refresh Profile View"):
        st.rerun()
    profile = db.get_user(user_id)
    st.json(profile.model_dump())

with col_main:
    st.subheader(f"⚡ Live Intelligence Feed: Top 5 Things to Know")
    st.write(f"*Currently curated for:* **{selected_role}**")
    
    if st.button("Generate Morning Briefing", type="primary"):
        with st.spinner("Scanning live global threat feeds and synthesizing strategic report..."):
            
            # We fetch hidden optimized keywords tied directly to that role
            hidden_query = PERSONAS[selected_role]["keywords"]
            style_instruction = PERSONAS[selected_role]["desc"]
            
            output_report = orchestrator.run(user_id, hidden_query, style_instruction)
            
            st.markdown("### 📰 Your Curated Security Briefing")
            st.info(output_report)
