from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from project_builder import build_and_run

app = FastAPI()

@app.post("/")
async def generate_code(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    auto_run = data.get("auto_run", False)
    try:
        build_and_run(prompt, auto_run)
        return JSONResponse({"message": "✅ Project generated successfully!"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
