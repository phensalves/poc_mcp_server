
from fastapi import FastAPI
from pydantic import BaseModel
from .python_analyzer import analyze

app = FastAPI()

class CodeAnalysisRequest(BaseModel):
    code: str

@app.post("/analyze")
async def analyze_code_endpoint(request: CodeAnalysisRequest):
    result = analyze(request.code)
    return {"analysis": result}
