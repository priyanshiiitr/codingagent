# project_builder.py
from ai_agent import generate_project_structure
from file_utils import create_project_from_json
import subprocess
import json
import sys
import os

def build_and_run(prompt, auto_run=False):
    print("\n🧠 Generating project files using Gemini...\n")

    data = generate_project_structure(prompt)
    if not data:
        print("❌ Failed to generate valid project data.")
        return

    main_file = create_project_from_json(data)  # create_project accepts dict or JSON string

    if auto_run and main_file:
        print(f"\n🚀 Running {main_file} ...\n")
        # use the same python interpreter as running this script
        subprocess.run([sys.executable, main_file])
