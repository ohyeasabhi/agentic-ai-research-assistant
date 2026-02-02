from local_llm import generate


# ---------------- Planner Agent ----------------
def plan_research(topic: str, model: str):
    prompt = f"""
You are a research planner.

Break the topic into EXACTLY 3 important subtopics.
Return them as bullet points.

Topic: {topic}
"""
    text = generate(prompt, model)
    return [line.strip("- ").strip() for line in text.split("\n") if line.strip()]


# ---------------- Researcher Agent ----------------
def research_subtopic(topic: str, subtopic: str, model: str):
    prompt = f"""
You are a research assistant.

Research the following subtopic concisely.

Main topic: {topic}
Subtopic: {subtopic}

Provide bullet points only.
"""
    return generate(prompt, model)


# ---------------- Writer Agent ----------------
def write_report(topic: str, notes: dict, model: str):
    combined = ""
    for subtopic, content in notes.items():
        combined += f"\n## {subtopic}\n{content}\n"

    prompt = f"""
You are a professional technical writer.

Write a well-structured research report in Markdown.

Topic: {topic}

Notes:
{combined}

Include:
- Short introduction
- Clear sections
- Concise conclusion
"""
    return generate(prompt, model)


# ---------------- Critic Agent ----------------
def critique_report(topic: str, report: str, model: str) -> str:
    prompt = f"""
You are a critical reviewer.

Evaluate the research report below.

Topic: {topic}

Report:
{report}

Respond with ONLY one word:
ACCEPT or RETRY
"""
    return generate(prompt, model).strip().upper()
