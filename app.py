import streamlit as st
from engine import AgentOrchestrator
from database import ProfileDB

st.set_page_config(page_title="Australian Cyber & Tech Intel", page_icon="🔒", layout="wide")

st.title("🇦🇺 Australian Cyber, Data & AI Intelligence Feed")
st.caption("Curated stateful threat intelligence wire specializing in the Australian digital ecosystem")

# Topic channels replacing the old persona setup
TOPICS = {
    "🔒 Cybersecurity & Incident Response": {
        "desc": "An authoritative threat assessment detailing ransomware incidents, local infrastructure compromises, ASD/ACSC advisories, critical CVE patch parameters, and technical mitigation paths impacting Australian organizations.",
        "keywords": "ransomware OR 'data breach' OR 'zero-day' OR credential OR malware"
    },
    "📊 Data Governance & Privacy Regulation": {
        "desc": "A data management briefing focused on Australian Privacy Principles (APPs), OAIC enforcement audits, corporate data retention parameters, corporate liability, and domestic consumer privacy metrics.",
        "keywords": "privacy OR OAIC OR 'Privacy Act' OR penalty OR retention OR governance"
    },
    "🤖 Emerging AI Safety & Governance": {
        "desc": "An emerging technology evaluation detailing shadow AI systems, localized large language model deployments, data poisoning vectors, and upcoming domestic AI safety policy guidelines.",
        "keywords": "AI OR LLM OR 'machine learning' OR algorithm OR deepfake OR regulation"
    }
}

user_id = "portfolio_user_demo"
orchestrator = AgentOrchestrator()
db = ProfileDB()

col_sidebar, col_main = st.columns([1, 2.5])

with col_sidebar:
    st.subheader("📋 Intelligence Channel Scope")
    selected_topic = st.selectbox("Select Target Stream:", list(TOPICS.keys()))
    
    st.divider()
    st.subheader("Persistent Profile State")
    if st.button("Refresh Profile View"):
        st.rerun()
    profile = db.get_user(user_id)
    st.json(profile.model_dump())

with col_main:
    st.subheader(f"📰 Curated National Wire Feed")
    st.write(f"Active Channel Lens: **{selected_topic}**")
    
    if st.button("Generate Strategic Briefing", type="primary"):
        with st.spinner("Scanning validated Australian technology news wire directories..."):
            
            hidden_query = TOPICS[selected_topic]["keywords"]
            style_instruction = TOPICS[selected_topic]["desc"]
            
            briefing_cards = orchestrator.run(user_id, hidden_query, style_instruction)
            
            st.markdown("### ⚡ Live Regional Intelligence Output")
            
            for idx, card in enumerate(briefing_cards, 1):
                with st.container():
                    st.markdown(f"#### {idx}. {card.get('title', 'No Title Available')}")
                    st.caption(f"🔍 Verified Resource: **{card.get('source', 'Premium Source')}**")
                    
                    display_text = card.get('summary') or card.get('description') or "Context unavailable."
                    st.info(display_text)
                    
                    card_url = card.get('url', '#')
                    if card_url != "#":
                        st.link_button("🔗 Read Original Verified Report", card_url)
                    
                    st.divider()
