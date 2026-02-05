🧠 Agentic AI Research Assistant (Local, Multi-Agent System)
A local, agentic AI research assistant built from scratch using Python and Streamlit, powered by open-source LLMs via Ollama.
This project demonstrates core Agentic AI concepts such as planning, tool usage, self-critique, semantic memory, and evaluation — all without paid APIs.
________________________________________
🚀 What This Project Is
This is not a chatbot.
It is a goal-driven agentic system that:
•	Plans how to approach a task
•	Breaks it into steps
•	Uses tools when needed
•	Reviews its own output
•	Improves results through retries
•	Remembers past knowledge semantically
Everything runs locally.
________________________________________
✨ Key Features
🧩 Agentic Architecture
•	Planner Agent – breaks a topic into subtopics
•	Researcher Agent – gathers information per subtopic
•	Writer Agent – synthesizes a structured report
•	Critic Agent – evaluates quality and triggers retries
🛠 Tool Usage
The agent can autonomously decide to use:
•	Persistent memory (save important knowledge)
•	Calculator (for numerical reasoning)
•	File writer (export results)
🧠 Memory Systems
•	Persistent Memory – topic → summary (JSON)
•	Semantic Memory – meaning-based recall using embeddings + FAISS
🔁 Self-Critique Loop
•	The agent reviews its own output
•	Retries generation if quality is insufficient
•	Stops when an acceptable result is achieved
📊 Evaluation & Logging
Each agent run logs:
•	Topic
•	Model used
•	Number of retries
•	Tools used
•	Execution time
Stored locally in agent_logs.json.
📄 Export
•	Download final research as Markdown
•	Download final research as PDF
________________________________________
🧠 Why This Is Agentic AI (Not Just LLM Usage)
This project demonstrates agent behavior, not prompt engineering.
✔ Planning before acting
✔ Role-based reasoning
✔ Tool awareness & execution
✔ Self-evaluation & retries
✔ Long-term semantic memory
✔ Observable decision metrics
These are the core building blocks of Agentic AI systems.
________________________________________
🏗 Architecture Overview
User (Streamlit UI)
   ↓
Agent Controller (app.py)
   ↓
Planner Agent
   ↓
Researcher Agent
   ↓
Writer Agent
   ↓
Critic Agent (retry loop)
   ↓
Tool Router
   ↓
Memory + Tools
   ↓
Semantic Vector Store (FAISS)
   ↓
Evaluation Logger
Each agent has one responsibility, coordinated by a central controller.
________________________________________
🛠 Tech Stack
•	Python
•	Streamlit – UI & orchestration
•	Ollama – local LLM runtime
•	Mistral / LLaMA / Neural-Chat – open-source LLMs
•	FAISS – vector similarity search
•	Sentence Transformers – embeddings
•	ReportLab – PDF generation
All components are free and local.
________________________________________
▶️ How to Run Locally
1️⃣ Install dependencies
pip install streamlit sentence-transformers faiss-cpu reportlab
2️⃣ Install and pull LLM
ollama pull mistral
3️⃣ Run the app
python -m streamlit run app.py
________________________________________
🧪 Example Use Cases
•	Research technical topics
•	Summarize complex subjects
•	Demonstrate agentic reasoning
•	Experiment with local LLMs
•	Study memory-augmented AI systems
________________________________________
📁 Project Structure
ai-research-assistant/
│
├── app.py                # Agent controller & UI
├── research_agent.py     # Planner, Researcher, Writer, Critic agents
├── tools.py              # Tool implementations & routing
├── semantic_memory.py    # Vector memory (FAISS)
├── agent_logger.py       # Evaluation & metrics logging
├── README.md
├── agent_logs.json       # (auto-generated)
________________________________________
📌 What This Project Demonstrates
•	Understanding of Agentic AI concepts
•	Clean separation of concerns
•	Local LLM deployment
•	Memory-augmented reasoning
•	Practical AI system design
•	Explainable, interview-ready architecture
________________________________________
🧠 Author Note
This project was built for educational and portfolio purposes, focusing on clarity, correctness, and real-world agent design rather than over-engineering or frameworks.
________________________________________
⭐ If You’re Reviewing This Repo
This project intentionally avoids:
•	Paid APIs
•	Heavy frameworks
•	Black-box abstractions
The goal is to demonstrate understanding, not hide logic.

