# file_utils.py
import os
import json

def create_project_from_json(json_or_dict, base_folder="generated_projects"):
    """
    Takes JSON (string) or a Python dict describing files and creates them
    in the workspace. Returns the path to the main file (if present).
    """
    os.makedirs(base_folder, exist_ok=True)

    if isinstance(json_or_dict, str):
        try:
            data = json.loads(json_or_dict)
        except json.JSONDecodeError:
            print("❌ Invalid JSON received.")
            return None
    elif isinstance(json_or_dict, dict):
        data = json_or_dict
    else:
        print("❌ Unsupported data type for project creation.")
        return None

    project_count = len([n for n in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, n))])
    project_folder = os.path.join(base_folder, f"project_{project_count + 1}")
    os.makedirs(project_folder, exist_ok=True)

    for path, content in data.get("files", {}).items():
        full_path = os.path.join(project_folder, path)
        os.makedirs(os.path.dirname(full_path) or ".", exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    main_file = data.get("main_file")
    print(f"\n✅ Project created in: {project_folder}")
    return os.path.join(project_folder, main_file) if main_file else None
