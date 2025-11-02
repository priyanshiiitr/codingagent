import subprocess
import os
import re

def git_commit_and_push(message="Auto commit by AI Agent", repo_url=None, base_dir="generated_projects"):
    """
    Add, commit, and push project files to a GitHub repository.
    If repo_url is provided, it sets the remote and pushes to it.
    Example:
        git_commit_and_push("Upload project", "https://github.com/user/repo.git")
    """

    try:
        # Move to the correct directory
        os.chdir(base_dir)

        # Initialize repo if needed
        if not os.path.exists(os.path.join(base_dir, ".git")):
            subprocess.run("git init", shell=True, check=True)
            print("🆕 Initialized new Git repository.")

        # Ensure main branch exists
        subprocess.run("git checkout -B main", shell=True, check=True)

        # Stage and commit
        subprocess.run("git add .", shell=True, check=True)
        subprocess.run(f'git commit -m "{message}"', shell=True)
        print("✅ Changes committed successfully.")

        # Set remote if repo URL is given
        if repo_url:
            subprocess.run("git remote remove origin", shell=True, stderr=subprocess.DEVNULL)
            subprocess.run(f"git remote add origin {repo_url}", shell=True, check=True)
            print(f"🔗 Linked remote repository: {repo_url}")

        # Push to GitHub (with fallback)
        push_result = subprocess.run("git push -u origin main", shell=True, text=True, capture_output=True)
        if "error" in push_result.stderr.lower():
            print("⚠️ Push failed, trying force push...")
            subprocess.run("git push -u origin main --force", shell=True, check=True)
        
        print("🚀 Project uploaded successfully to GitHub!")

    except subprocess.CalledProcessError as e:
        print("❌ Git command failed:", e)
    except Exception as e:
        print("❌ Unexpected error:", str(e))
