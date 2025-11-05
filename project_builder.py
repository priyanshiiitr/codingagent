# project_builder.py

from ai_agent import generate_project_structure
from file_utils import create_project_from_json
import subprocess
import json
import sys
import os
import zipfile
import io
import base64
import requests


def build_and_run(prompt, auto_run=False, github_enabled=False,
                  github_username=None, github_repo=None, github_pat=None):
    """
    Generates project, optionally auto-runs it (local only),
    and optionally uploads to GitHub if user enables it via Streamlit UI.

    Returns: ZIP file bytes (for Streamlit's download button)
    """

    print("\n🧠 Generating project files using Gemini...\n")

    data = generate_project_structure(prompt)
    if not data:
        print("❌ Failed to generate valid project data.")
        return None

    # Create project in VS Code workspace (local machine)
    project_folder = create_project_from_json(data)
    print(f"✅ Project generated at: {project_folder}")

    # ----------------------------
    # ZIP the generated project
    # ----------------------------
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, project_folder))

    zip_buffer.seek(0)

    # ----------------------------
    # Optional: Upload to GitHub
    # ----------------------------
    if github_enabled and github_username and github_repo and github_pat:
        print("📤 Uploading project to GitHub...")
        upload_to_github(zip_buffer, github_username, github_repo, github_pat)

    # ----------------------------
    # Optional: Auto-run main file
    # ----------------------------
    main_file = data.get("main_file")
    if auto_run and main_file:
        main_path = os.path.join(project_folder, main_file)
        print(f"\n🚀 Running {main_path}\n")
        subprocess.run([sys.executable, main_path])

    return zip_buffer.getvalue()


def upload_to_github(zip_buffer, username, repo_name, token):
    """
    Uploads ZIP project contents to GitHub using GitHub REST API.
    User must enter PAT token in Streamlit UI.
    """

    headers = {"Authorization": f"Bearer {token}"}

    # ✅ Create repo if not exists
    requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json={"name": repo_name, "private": False}
    )

    # ✅ Upload each file inside the zip
    with zipfile.ZipFile(zip_buffer, "r") as zip_ref:
        for file_path in zip_ref.namelist():
            file_data = zip_ref.read(file_path).decode("utf-8")

            url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{file_path}"
            payload = {
                "message": f"Add {file_path}",
                "content": base64.b64encode(file_data.encode()).decode()
            }

            requests.put(url, headers=headers, json=payload)

    print("✅ Upload complete!")
