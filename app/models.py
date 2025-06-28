from pydantic import BaseModel
from typing import List, Dict, Any


class Issue(BaseModel):
    code: str
    message: str
    line_number: int


class AnalysisReport(BaseModel):
    metrics: Dict[str, Any]
    issues: List[Issue]
    # You could add more fields here, like refactoring_suggestions, etc.
