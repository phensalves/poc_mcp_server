from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import importlib
import httpx
from .llm_providers.base import LLMProvider
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()


# --- Plugin & Provider Loading ---


def load_language_analyzers():
    plugins = {}
    plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
    for filename in os.listdir(plugin_dir):
        if filename.endswith("_plugin.py"):
            module_name = f"app.plugins.{filename[:-3]}"
            plugin_module = importlib.import_module(module_name)
            if hasattr(plugin_module, "analyze"):
                # Key is the language name from the filename (e.g., 'python')
                plugins[filename.split("_")[0]] = plugin_module.analyze
    return plugins


def load_llm_providers():
    providers = {}
    provider_dir = os.path.join(os.path.dirname(__file__), "llm_providers")
    for filename in os.listdir(provider_dir):
        if (
            filename.endswith(".py")
            and not filename.startswith("__")
            and filename != "base.py"
        ):
            module_name = f"app.llm_providers.{filename[:-3]}"
            module = importlib.import_module(module_name)
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (
                    isinstance(item, type)
                    and issubclass(item, LLMProvider)
                    and item is not LLMProvider
                ):
                    instance = item()
                    providers[instance.get_name()] = instance
    return providers


# --- Data Models ---


class AnalysisRequest(BaseModel):
    language: str
    code: str
    provider: str = "mock"


# --- Loaders ---


language_analyzers = load_language_analyzers()
llm_providers = load_llm_providers()


# --- API Endpoints ---


@app.post("/analyze")
async def analyze_code(request: AnalysisRequest):
    if request.provider not in llm_providers:
        raise HTTPException(
            status_code=400,
            detail=f"LLM Provider '{request.provider}' not supported."
        )

    llm_provider = llm_providers[request.provider]
    refactoring_suggestion = llm_provider.get_refactoring_suggestion(
        request.code
    )
    analysis_result = {}

    if request.language == "python":
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://python_analyzer:8001/analyze",
                    json={"code": request.code}
                )
                response.raise_for_status()
                analysis_result = response.json()["analysis"]
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Error communicating with Python Analyzer: {exc}",
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Python Analyzer error: {exc.response.text}",
            )
    elif request.language in language_analyzers:
        analyzer_func = language_analyzers[request.language]
        analysis_result = analyzer_func(request.code)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Language '{request.language}' not supported."
        )

    analysis_result["refactoring_suggestion"] = refactoring_suggestion

    return {"language": request.language, "analysis": analysis_result}


@app.get("/supported-languages")
async def get_supported_languages():
    return {"languages": list(language_analyzers.keys())}


@app.get("/supported-providers")
async def get_supported_providers():
    return {"providers": list(llm_providers.keys())}


# --- Static File Serving ---
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def read_index():
<<<<<<< HEAD
    return FileResponse("frontend/index.html")
=======
    return FileResponse("frontend/index.html")
>>>>>>> a21f4a7 (fix(lint): Resolve E501 flake8 warnings in app/main.py)
