# main.py
from project_builder import build_and_run
from ai_agent import handle_user_prompt

print("\n🤖 Advanced AI Code Agent — Multi-File Project Builder\n")
print("You have two modes:")
print("1) 'generate' - create a full project using the project builder")
print("2) 'agent' - ask the tool-using agent to act (edit, run, git, generate)\n")
print("Type 'exit' to quit.\n")

while True:
    mode = input("Mode (generate/agent) >>> ").strip().lower()
    if mode == "exit":
        break
    if mode not in ("generate", "agent"):
        print("Choose 'generate' or 'agent'.")
        continue

    prompt = input("🧠 Prompt >>> ")
    if prompt.lower() == "exit":
        break

    if mode == "generate":
        auto_run = input("Run after generation? (y/n): ").strip().lower() == "y"
        build_and_run(prompt, auto_run)
    else:
        result = handle_user_prompt(prompt)
        print("\nResult:\n", result)
