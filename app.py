import streamlit as st
import time
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from research_agent import (
    plan_research,
    research_subtopic,
    write_report,
    critique_report
)

from tools import (
    load_memory,
    route_tool,
    save_memory,
    calculator,
    write_file
)

from semantic_memory import add_to_memory, search_memory
from agent_logger import log_run


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide"
)

# ---------------- Session State ----------------
defaults = {
    "final_report": None,
    "research_done": False,
    "plan": [],
    "notes": {},
    "history": [],
    "model": "mistral",
    "related_memories": [],
    "tools_used": [],
    "start_time": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("🧠 AI Research Assistant")

    st.markdown("### 🔀 Model")
    st.session_state.model = st.selectbox(
        "Choose LLM",
        ["mistral", "llama2", "neural-chat"],
        index=0
    )

    st.divider()
    st.markdown("### 🧠 Persistent Memory")

    memory = load_memory()
    if memory:
        for k in list(memory.keys())[-5:]:
            st.caption(f"• {k}")
    else:
        st.caption("No saved memories yet")

    st.divider()
    st.markdown("### 🧠 Semantic Memory")

    if st.session_state.related_memories:
        for m in st.session_state.related_memories:
            st.caption(m[:80] + "...")
    else:
        st.caption("No related knowledge found")

    st.divider()
    reset = st.button("🔄 Start New Research")


# ---------------- Reset ----------------
if reset:
    st.session_state.final_report = None
    st.session_state.research_done = False
    st.session_state.plan = []
    st.session_state.notes = {}
    st.session_state.related_memories = []
    st.session_state.tools_used = []
    st.rerun()


# ---------------- Main UI ----------------
st.title("🔍 Research a Topic")

topic = st.text_input(
    "Enter a topic",
    placeholder="e.g. Quantum Computing, Climate Change, Large Language Models"
)

run = st.button("🚀 Research")


# ---------------- Agent Execution ----------------
if run and topic.strip() and not st.session_state.research_done:

    st.session_state.start_time = time.time()
    st.session_state.tools_used = []
    progress = st.progress(0)

    # ---- Semantic memory recall ----
    st.session_state.related_memories = search_memory(topic)

    memory_context = ""
    if st.session_state.related_memories:
        memory_context = "\n\nRelevant past research:\n"
        for m in st.session_state.related_memories:
            memory_context += f"- {m}\n"

    # ---- Planner Agent ----
    st.session_state.plan = plan_research(
        topic + memory_context,
        st.session_state.model
    )
    progress.progress(25)

    st.subheader("🗺 Research Plan")
    for s in st.session_state.plan:
        st.write(f"- {s}")

    # ---- Researcher Agent ----
    st.session_state.notes = {}

    for idx, subtopic in enumerate(st.session_state.plan):
        notes = research_subtopic(topic, subtopic, st.session_state.model)
        st.session_state.notes[subtopic] = notes

        with st.expander(f"Notes: {subtopic}"):
            st.markdown(notes)

        progress.progress(25 + int((idx + 1) / len(st.session_state.plan) * 50))

    # ---- Writer + Critic Loop ----
    with st.spinner("🧠 Writing & reviewing final report..."):
        MAX_RETRIES = 2
        attempt = 0
        final_text = ""

        while attempt <= MAX_RETRIES:
            llm_output = write_report(
                topic, st.session_state.notes, st.session_state.model
            )

            tool = None
            tool, result = route_tool(llm_output)

            if tool == "save_memory":
                final_text = result.get("summary", "")
            else:
                final_text = result

            verdict = critique_report(
                topic, final_text, st.session_state.model
            )

            if verdict == "ACCEPT":
                break

            attempt += 1

        # ---- Tool Execution ----
        if tool == "save_memory":
            save_memory(topic, final_text)
            st.session_state.tools_used.append("save_memory")

        elif tool == "calculator":
            final_text = f"Calculation result: {calculator(result.get('expression', ''))}"
            st.session_state.tools_used.append("calculator")

        elif tool == "write_file":
            final_text = write_file(
                result.get("filename", "output.txt"),
                result.get("content", "")
            )
            st.session_state.tools_used.append("write_file")

        # ---- Semantic Memory ----
        add_to_memory(final_text)

        # ---- Logging ----
        duration = time.time() - st.session_state.start_time
        log_run(
            topic=topic,
            model=st.session_state.model,
            retries=attempt,
            tools_used=st.session_state.tools_used,
            duration_sec=duration
        )

        st.session_state.final_report = final_text
        st.session_state.research_done = True
        st.session_state.history.append(topic)

    progress.progress(100)


# ---------------- Output ----------------
if st.session_state.final_report:
    st.divider()
    st.subheader("📄 Final Research Summary")
    st.markdown(st.session_state.final_report)

    md_bytes = BytesIO(st.session_state.final_report.encode("utf-8"))
    st.download_button(
        "⬇️ Download Markdown",
        md_bytes,
        file_name=f"{topic.replace(' ', '_').lower()}.md",
        mime="text/markdown"
    )

    pdf_buffer = BytesIO()
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_buffer)
    story = [
        Paragraph(p, styles["Normal"])
        for p in st.session_state.final_report.split("\n")
        if p.strip()
    ]
    doc.build(story)

    st.download_button(
        "⬇️ Download PDF",
        pdf_buffer.getvalue(),
        file_name=f"{topic.replace(' ', '_').lower()}.pdf",
        mime="application/pdf"
    )
