import subprocess
import os

def git_commit_and_push(message="Auto commit by AI Agent", repo_url=None):
    """
    Automatically initialize git, remove old origin if exists,
    add new origin, commit, and push changes to the given repository.
    """
    try:
        # Move into the generated project folder
        if not os.path.isdir("generated_projects"):
            print("❌ No generated_projects folder found.")
            return "❌ No project folder found to upload."

        os.chdir("generated_projects")

        # If there are multiple subprojects, pick the latest one
        subfolders = sorted(
            [d for d in os.listdir(".") if os.path.isdir(d)],
            key=lambda x: os.path.getmtime(x),
            reverse=True
        )
        target_folder = subfolders[0] if subfolders else "."
        os.chdir(target_folder)

        print(f"📂 Using folder: {os.getcwd()}")

        # Initialize git repo if not already
        subprocess.run("git init", shell=True, check=False)

        # Remove old remote origin if exists
        subprocess.run("git remote remove origin", shell=True, check=False)

        # Add the new remote
        if repo_url:
            subprocess.run(f'git remote add origin {repo_url}', shell=True, check=True)

        # Stage, commit, and push
        subprocess.run("git add .", shell=True, check=True)
        subprocess.run(f'git commit -m "{message}"', shell=True, check=True)

        # Push to 'main' branch, creating it if necessary
        subprocess.run("git branch -M main", shell=True, check=False)
        subprocess.run("git push -u origin main --force", shell=True, check=True)

        print(f"✅ Successfully pushed to {repo_url}")
        os.chdir("../..")  # Return to root directory
        return f"✅ Successfully uploaded project to {repo_url}"

    except subprocess.CalledProcessError as e:
        os.chdir("../..")
        return f"❌ Git operation failed: {e}"
    except Exception as e:
        os.chdir("../..")
        return f"❌ Unexpected error: {e}"
