import json
from pathlib import Path

MEMORY_FILE = Path("agent_memory.json")


def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {}


def save_memory(topic: str, summary: str):
    memory = load_memory()
    memory[topic] = summary
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))


def calculator(expression: str):
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression"


def write_file(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File '{filename}' written successfully."


def route_tool(llm_output: str):
    """
    Parses LLM output to decide whether to call a tool.
    """
    if llm_output.startswith("TOOL:"):
        lines = llm_output.splitlines()
        tool_name = lines[0].replace("TOOL:", "").strip()

        args = {}
        for line in lines[2:]:
            if "=" in line:
                k, v = line.split("=", 1)
                args[k.strip()] = v.strip()

        return tool_name, args

    return None, llm_output
