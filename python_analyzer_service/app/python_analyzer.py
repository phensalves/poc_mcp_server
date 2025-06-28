
import ast

def analyze(code: str):
    """Analyzes a snippet of Python code."""
    report = {
        "metrics": {},
        "issues": []
    }

    try:
        tree = ast.parse(code)
        report["metrics"]["node_count"] = len(list(ast.walk(tree)))

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20: # Arbitrary threshold
                    report["issues"].append(
                        f"Function '{node.name}' is too long ({len(node.body)} lines). Consider refactoring."
                    )
    except SyntaxError as e:
        report["issues"].append(f"Syntax Error: {e}")

    return report
