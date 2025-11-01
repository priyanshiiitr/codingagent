import subprocess

def git_commit_and_push(message="Auto commit by AI Agent"):
    """
    Automatically add, commit, and push changes.
    """
    try:
        subprocess.run("git add .", shell=True, check=True)
        subprocess.run(f'git commit -m "{message}"', shell=True, check=True)
        subprocess.run("git push", shell=True, check=True)
        print("✅ Changes committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Git operation failed:", str(e))
