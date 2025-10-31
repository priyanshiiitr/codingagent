import google.generativeai as genai
from config import API_KEY, MODEL_NAME
import re
import json

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def extract_json(text):
    """
    Extract JSON from Gemini response (even if it includes markdown or extra text).
    """
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            print("⚠️ JSON parsing failed. Trying cleanup...")
            cleaned = match.group().replace("```json", "").replace("```", "")
            return json.loads(cleaned)
    return None


def generate_project_structure(prompt):
    """
    Ask Gemini to return a clean JSON containing files and code.
    """
    instruction = f"""
    You are an expert AI code generator.
    Generate ONLY valid JSON (no markdown, no text outside JSON).

    Example format:
    {{
        "files": {{
            "app.py": "# Flask app code...",
            "templates/index.html": "<html>...</html>",
            "static/script.js": "// JS code..."
        }},
        "main_file": "app.py"
    }}

    Task: {prompt}
    """

    response = model.generate_content(instruction)
    print("✅ Gemini responded. Parsing JSON...\n")
    data = extract_json(response.text)
    if not data:
        print("❌ Could not parse JSON. Here’s what Gemini sent:\n", response.text)
    return data
