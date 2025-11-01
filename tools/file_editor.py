import os
import google.generativeai as genai
from config import API_KEY, MODEL_NAME

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def modify_file(file_path, modification_prompt):
    """
    Modify an existing file based on a natural language instruction using Gemini.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    instruction = f"""
    Modify the following code according to the user's request.
    Keep the same structure and language.
    
    Request: {modification_prompt}

    Original Code:
    ```
    {original_code}
    ```
    Return only the modified code (no explanations, no markdown).
    """

    response = model.generate_content(instruction)
    new_code = response.text.strip().replace("```python", "").replace("```", "")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_code)

    print(f"✅ File '{file_path}' updated successfully.")
