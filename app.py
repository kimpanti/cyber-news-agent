import streamlit as st
from engine import AgentOrchestrator
from database import ProfileDB

st.set_page_config(page_title="Cyber Intelligence News Agent", page_icon="🔒")
st.title("🔒 Cyber, Privacy & AI News Agent")
st.caption("Adaptive multi-persona news synthesis engine powered by LangChain & GPT-4o-mini")

PERSONAS = {
    "👶 Explain Like I'm 5": "A five-year-old child. Eliminate all jargon. Use physical, real-world schoolyard analogies.",
    "👔 Corporate Executive": "A busy C-Level executive. Bullet points only. Highlight strategic business risk, legal liability, and mitigation.",
    "💻 Lead Security Engineer": "A highly technical staff engineer. Focus on underlying technical mechanics, CVE references, and architectural controls.",
    "⚖️ Privacy Compliance Auditor": "A data privacy attorney. Focus heavily on regulatory violations, international frameworks (GDPR, CCPA), and governance metrics."
}

user_id = "portfolio_user_demo"
orchestrator = AgentOrchestrator()
db = ProfileDB()

with st.sidebar:
    st.subheader("Persistent Profile State")
    if st.button("Refresh Profile View"):
        st.rerun()
    profile = db.get_user(user_id)
    st.json(profile.model_dump())

topic = st.text_input("Enter a technical topic or trend:", placeholder="e.g., Apple passkey deployment hurdles, zero-day data exfiltration")
selected_label = st.selectbox("Select Explanation Persona Lens:", list(PERSONAS.keys()))

if st.button("Fetch & Synthesize News", type="primary"):
    if not topic.strip():
        st.warning("Please enter an active search topic first.")
    else:
        with st.spinner("Executing secure retrieval tools and adjusting persona layers..."):
            output_report = orchestrator.run(user_id, topic, PERSONAS[selected_label])
            st.markdown("### Agent Synthesis Output")
            st.info(output_report)
