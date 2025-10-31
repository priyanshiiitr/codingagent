from ai_agent import generate_project_structure
from file_utils import create_project_from_json
import subprocess
import json

def build_and_run(prompt, auto_run=False):
    print("\n🧠 Generating project files using Gemini...\n")

    # Step 1: Generate project data from Gemini
    data = generate_project_structure(prompt)
    if not data:
        print("❌ Failed to generate valid project data.")
        return

    # Step 2: Create the files from the JSON data
    main_file = create_project_from_json(json.dumps(data))

    # Step 3: Optionally auto-run the main file
    if auto_run and main_file:
        print(f"\n🚀 Running {main_file} ...\n")
        subprocess.run(["python", main_file], shell=True)
