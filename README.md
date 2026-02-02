# 🧠 AI Research Assistant (Agentic AI)

A local, agentic AI research assistant built using Python, Streamlit, and open-source LLMs.
The system uses multiple agent roles, tool routing, semantic memory, and self-critique to produce high-quality research outputs.

---

## ✨ Features

- Planner → Researcher → Writer → Critic agents
- Local LLMs via Ollama (Mistral, LLaMA, Neural-Chat)
- Tool usage (memory, calculator, file writer)
- Self-critique with retry loop
- Persistent memory + semantic vector memory (FAISS)
- Agent evaluation & logging
- Markdown & PDF export
- Fully offline and free

---

## 🧠 Architecture Overview

User → Controller → Planner → Researcher → Writer → Critic  
                                     ↓  
                                Tools & Memory  

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
ollama pull mistral
python -m streamlit run app.py
    