from project_builder import build_and_run

print("\n🤖 Advanced AI Code Agent — Multi-File Project Builder\n")
print("Type natural language commands like:\n")
print("> create a flask app with index.html and a route that displays 'Hello IIIT Raichur!'\n")
print("> make a web scraper that saves quotes into CSV\n")
print("Type 'exit' to quit.\n")

while True:
    prompt = input("🧠 Prompt >>> ")
    if prompt.lower() == "exit":
        break

    auto_run = input("Run after generation? (y/n): ").strip().lower() == "y"
    build_and_run(prompt, auto_run)
