# ai_agent.py
import google.generativeai as genai
from config import API_KEY, MODEL_NAME
import re
import json
import os
import subprocess
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

# tools
from tools.file_editor import modify_file
from tools.git_manager import git_commit_and_push
from tools.command_runner import run_command

# === Gemini setup ===
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# === Memory persistence ===
MEMORY_DIR = "memory"
MEMORY_FILE = os.path.join(MEMORY_DIR, "agent_memory.json")
os.makedirs(MEMORY_DIR, exist_ok=True)

# Initialize LangChain memory (runtime)
memory = ConversationBufferMemory(return_messages=True)

def load_memory():
    """Load persisted memory from disk into the runtime langchain memory."""
    if not os.path.exists(MEMORY_FILE):
        return
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)  # list of {"role": "user"/"ai", "content": "..."}
        for m in messages:
            if m.get("role") == "user":
                memory.chat_memory.add_message(HumanMessage(content=m.get("content", "")))
            else:
                memory.chat_memory.add_message(AIMessage(content=m.get("content", "")))
        print(f"✅ Loaded {len(messages)} messages from memory.")
    except Exception as e:
        print("⚠️ Failed to load memory:", e)

def save_memory():
    """Persist current memory messages to disk as a simple JSON list."""
    try:
        msgs = []
        for m in memory.chat_memory.messages:
            role = "user" if isinstance(m, HumanMessage) else "ai"
            msgs.append({"role": role, "content": m.content})
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(msgs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("⚠️ Failed to save memory:", e)

# Load memory at import time
load_memory()

# === Helper: JSON extractor ===
def extract_json(text):
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            cleaned = match.group().replace("```json", "").replace("```", "")
            try:
                return json.loads(cleaned)
            except Exception:
                return None
    return None

# === Helper: find files in generated_projects ===
def find_in_generated_projects(filename, base="generated_projects"):
    """
    Search for filename recursively inside `base`. Return first match full path or None.
    """
    if not os.path.isdir(base):
        return None
    # Normalize filename
    filename = os.path.basename(filename)
    for root, dirs, files in os.walk(base):
        if filename in files:
            return os.path.join(root, filename)
    return None

# === Core: Project generator ===
def generate_project_structure(prompt):
    instruction = f"""
You are an expert AI code generator.
Generate ONLY valid JSON (no markdown, no text outside JSON).

Example format:
{{
    "files": {{
        "app.py": "# Flask app code...",
        "templates/index.html": "<html>...</html>",
        "static/script.js": "// JS code..."
    }},
    "main_file": "app.py"
}}

Task: {prompt}
"""
    try:
        response = model.generate_content(instruction)
    except Exception as e:
        print("❌ Gemini request failed:", e)
        return None

    data = extract_json(response.text)
    if not data:
        print("❌ Could not parse JSON. Here’s what Gemini sent:\n", response.text)
    else:
        print("✅ Gemini responded and parsed successfully.")
    return data

# === Tool Selector ===
def choose_tool(user_prompt, conversation_context):
    instruction = f"""
You are an intelligent AI agent controller with MEMORY.

You have access to the following tools:
1. file_editor – to modify existing files.
2. command_runner – to execute shell or terminal commands.
3. git_manager – to commit and push code.
4. project_generator – to create or generate new projects from scratch.

Here is the previous conversation for context:
{conversation_context}

Decide which ONE tool should be used for this user request:
"{user_prompt}"

Respond in pure JSON only:
{{
    "tool": "file_editor" | "command_runner" | "git_manager" | "project_generator",
    "args": {{
        "file_path": "optional, if editing a file",
        "modification_prompt": "optional, if editing a file",
        "cmd": "optional, if running command",
        "message": "optional, if doing git commit"
    }}
}}
"""
    try:
        response = model.generate_content(instruction)
    except Exception as e:
        print("❌ Gemini tool-choice request failed:", e)
        return None

    data = extract_json(response.text)
    if not data:
        print("⚠️ Could not parse tool choice:\n", response.text)
    return data

# === Master Controller ===
def handle_user_prompt(prompt):
    """
    Main function: interprets prompt, picks tool, executes it with memory.
    Returns the result string of the executed tool.
    """
    # Add user message to memory
    memory.chat_memory.add_message(HumanMessage(content=prompt))

    # Prepare conversation context for LLM
    history = "\n".join(
        [f"User: {m.content}" if isinstance(m, HumanMessage) else f"AI: {m.content}" for m in memory.chat_memory.messages]
    )

    # Let Gemini choose tool intelligently
    tool_data = choose_tool(prompt, history)
    if not tool_data or "tool" not in tool_data:
        print("❌ No valid tool detected. Defaulting to project generation.")
        tool_data = {"tool": "project_generator", "args": {}}

    tool = tool_data["tool"]
    args = tool_data.get("args", {})

    print(f"\n🧠 Selected Tool: {tool}\n")

    # Execute tool and capture result message
    result = None
    try:
        if tool == "file_editor":
            # Get provided args
            file_path_arg = str(args.get("file_path", "")).strip()
            mod_prompt = str(args.get("modification_prompt", "")).strip()

            target_path = None
            result = None

            # If exact path provided and exists, use it
            if file_path_arg and os.path.exists(file_path_arg):
                target_path = file_path_arg
                print(f"ℹ️ Using exact path provided: {target_path}")
            else:
                # If user provided something that looks like a path but doesn't exist,
                # try to intelligently resolve
                if file_path_arg:
                    # If they gave a filename only (app.py) or an incomplete path (generated_projects app.py)
                    basename = os.path.basename(file_path_arg)
                    guessed = find_in_generated_projects(basename)
                    if guessed:
                        target_path = guessed
                        print(f"ℹ️ Auto-resolved '{file_path_arg}' -> '{guessed}'")
                    else:
                        # If they passed something like "generated_projects app.py" we try extract last token as filename
                        tokens = file_path_arg.split()
                        if len(tokens) > 1:
                            possible = tokens[-1]
                            guessed2 = find_in_generated_projects(possible)
                            if guessed2:
                                target_path = guessed2
                                print(f"ℹ️ Auto-resolved '{file_path_arg}' -> '{guessed2}'")
                # If still no file path, try extract a filename from the modification prompt itself
                if not target_path and not file_path_arg and mod_prompt:
                    m = re.search(r'([A-Za-z0-9_\-]+\.(py|html|css|js|json|md))', mod_prompt)
                    if m:
                        filename_from_prompt = m.group(1)
                        guessed3 = find_in_generated_projects(filename_from_prompt)
                        if guessed3:
                            target_path = guessed3
                            print(f"ℹ️ Auto-resolved filename from prompt -> '{guessed3}'")

                # As a last fallback, if user asked to edit "app.py" without path, search for app.py
                if not target_path and not file_path_arg:
                    # attempt to find a common file name (e.g., app.py)
                    m2 = re.search(r'\b(app\.py|main\.py|index\.html|templates/index.html)\b', mod_prompt)
                    if m2:
                        guessed4 = find_in_generated_projects(m2.group(0))
                        if guessed4:
                            target_path = guessed4
                            print(f"ℹ️ Auto-resolved common filename from prompt -> '{guessed4}'")

            if not target_path:
                # Nothing found; produce helpful message
                msg = "❌ File not found. Provide a full path like 'generated_projects/project_1/app.py' or run 'list generated_projects' first."
                print(msg)
                result = msg
            else:
                # Call tool to modify file
                result = modify_file(target_path, mod_prompt)

        elif tool == "command_runner":
            cmd = args.get("cmd", "")
            result = run_command(cmd)
        elif tool == "git_manager":
            message = args.get("message", "Auto commit by AI Agent")
            result = git_commit_and_push(message)
        elif tool == "project_generator":
            data = generate_project_structure(prompt)
            if data:
                # use file_utils.create_project_from_json if desired; simple write here
                base_folder = "generated_projects"
                os.makedirs(base_folder, exist_ok=True)
                project_count = len([n for n in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, n))])
                project_folder = os.path.join(base_folder, f"project_{project_count + 1}")
                os.makedirs(project_folder, exist_ok=True)
                for path, code in data.get("files", {}).items():
                    full_path = os.path.join(project_folder, path)
                    os.makedirs(os.path.dirname(full_path) or ".", exist_ok=True)
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(code)
                result = f"✅ Project created at: {project_folder}. Main file: {data.get('main_file','')}"
            else:
                result = "❌ Project generation failed."
        else:
            result = "❌ Unknown tool selected."
    except Exception as e:
        result = f"❌ Error while executing tool: {e}"

    # Store AI response and the tool result in memory and persist
    memory.chat_memory.add_message(AIMessage(content=f"Used tool: {tool}\nResult: {str(result)}"))
    save_memory()

    return result
