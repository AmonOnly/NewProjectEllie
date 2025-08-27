import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def add_entry(command, tool, args, result, feedback=None):
    memory = load_memory()
    entry = {
        "command": command,
        "tool": tool,
        "args": args,
        "result": result,
        "feedback": feedback
    }
    memory.append(entry)
    save_memory(memory)

def get_last_commands(n=5):
    memory = load_memory()
    return memory[-n:]
a