# 🔒 Cyber, Privacy & AI News Agent

An adaptive, multi-persona news synthesis engine built with **LangChain**, **Streamlit**, and **GPT-4o-mini**. This agent dynamically fetches real-time tech, cybersecurity, and AI governance updates and rewrites them tailored to specific user-selected cognitive levels (e.g., ELI5, Corporate Executive, Lead Security Engineer).

## 🚀 Key Features
- **Stateful User Profiling:** Automatically tracks user topic interests and preference weights over time using a lightweight JSON state layer.
- **Guardrailed Retrieval:** Constrains live NewsAPI queries to strict cybersecurity, privacy, and data governance bounds.
- **Dynamic Persona Conditioning:** Transforms complex technical payloads into target communication styles on the fly.
