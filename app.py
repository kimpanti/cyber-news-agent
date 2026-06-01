import streamlit as st
from engine import AgentOrchestrator
from database import ProfileDB

st.set_page_config(page_title="Cyber Intelligence Briefing Engine", page_icon="🔒", layout="wide")

# FIX: Flat, sanitized string block to completely prevent hidden character TypeErrors
st.markdown("""
<style>
.news-card {
    background-color: #1e293b;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    border-left: 5px solid #3b82f6;
}
.source-badge {
    background-color: #334155;
    color: #94a3b8;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
}
</style>
""", unsafe_allowed_html=True)

st.title("🔒 Cyber, Privacy & AI Security Intelligence Feed")
st.caption("Automated threat intelligence and regulatory curation engine powered by LangChain & Groq")

PERSONAS = {
    "👔 Chief Information Security Officer (CISO)": {
        "desc": "A high-level executive briefing focused on systemic threat trends, material financial risk, vendor vulnerabilities, and business continuity metrics. Bold statements only.",
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

col_sidebar, col_main = st.columns([1, 2.5])

with col_sidebar:
    st.subheader("📋 Profile Workspace Configuration")
    selected_role = st.selectbox("Select Target User Lens Profile:", list(PERSONAS.keys()))
    
    st.markdown("---")
    st.subheader("Persistent Profile State")
    if st.button("Refresh Profile View"):
        st.rerun()
    profile = db.get_user(user_id)
    st.json(profile.model_dump())

with col_main:
    st.subheader("📰 Live Threat Intel Feed: Top 5 Things to Know")
    st.write(f"Tailored for: **{selected_role}**")
    
    if st.button("Generate Morning Intelligence Briefing", type="primary"):
        with st.spinner("Scanning global threat feeds and parsing metadata records..."):
            
            hidden_query = PERSONAS[selected_role]["keywords"]
            style_instruction = PERSONAS[selected_role]["desc"]
            
            briefing_cards = orchestrator.run(user_id, hidden_query, style_instruction)
            
            st.markdown("### ⚡ Live Intelligence Curation Wire")
            
            for idx, card in enumerate(briefing_cards, 1):
                with st.container():
                    st.markdown(f"#### {idx}. {card.get('title', 'No Title Available')}")
                    st.markdown(f"<span class='source-badge'>🔍 Resource: {card.get('source', 'Unknown Source')}</span>", unsafe_allowed_html=True)
                    st.write("") 
                    
                    display_text = card.get('summary') or card.get('description') or "No contextual brief available for this record."
                    st.info(display_text)
                    
                    card_url = card.get('url', '#')
                    if card_url != "#":
                        st.link_button(f"🔗 Verify Raw Resource Wire", card_url)
                    
                    st.markdown("---")
