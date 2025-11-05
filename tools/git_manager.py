# tools/git_manager.py
import os
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")


def create_github_repo(repo_name, description="Repo created by AI Coding Agent"):
    """Create a GitHub repo using GitHub API."""
    api_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "name": repo_name,
        "description": description,
        "private": False
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 201:
        repo = response.json()
        print(f"✅ GitHub repo created successfully: {repo['html_url']}")
        return repo["clone_url"], repo["html_url"]

    print(f"❌ GitHub repo creation failed: {response.text}")
    return None, None


def git_commit_and_push(folder_path, message="Auto commit by AI Agent"):
    """Push project to GitHub + return repo links (ZIP + Codespaces)."""
    repo_name = os.path.basename(folder_path)

    # ✅ Create GitHub repo
    clone_url, html_url = create_github_repo(repo_name)

    if not clone_url:
        return "❌ Failed to create GitHub repo."

    # ZIP download + Codespaces
    zip_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}/archive/refs/heads/main.zip"
    codespaces_url = f"https://github.com/codespaces/new?repo={GITHUB_USERNAME}/{repo_name}"

    os.chdir(folder_path)
    try:
        subprocess.run("git init", shell=True, check=False)
        subprocess.run("git add .", shell=True, check=True)
        subprocess.run(f'git commit -m "{message}"', shell=True, check=True)
        subprocess.run("git branch -M main", shell=True, check=False)

        # ✅ Force replace origin
        subprocess.run("git remote remove origin", shell=True, check=False)
        subprocess.run(f"git remote add origin {clone_url}", shell=True, check=True)

        subprocess.run("git push -u origin main --force", shell=True, check=True)

        print(f"✅ Code pushed to GitHub: {html_url}")

        return {
            "repo_url": html_url,
            "zip_url": zip_url,
            "codespaces_url": codespaces_url
        }

    except subprocess.CalledProcessError as e:
        return f"❌ Git push failed: {e}"

    finally:
        os.chdir("../..")
