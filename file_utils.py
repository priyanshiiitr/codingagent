import os
import json

def create_project_from_json(json_str, base_folder="generated_projects"):
    """
    Takes JSON describing files and creates them in the workspace.
    """

    # ✅ Ensure the base folder exists
    os.makedirs(base_folder, exist_ok=True)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print("❌ Invalid JSON received from Gemini.")
        return None

    # Create a unique subfolder for the project
    project_count = len(os.listdir(base_folder))
    project_folder = os.path.join(base_folder, f"project_{project_count + 1}")
    os.makedirs(project_folder, exist_ok=True)

    # ✅ Create all files as per Gemini response
    for path, content in data.get("files", {}).items():
        full_path = os.path.join(project_folder, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    main_file = data.get("main_file")
    print(f"\n✅ Project created in: {project_folder}")
    return os.path.join(project_folder, main_file) if main_file else None
