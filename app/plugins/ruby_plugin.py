import re
from typing import Dict, List, Any


def analyze(code: str) -> Dict[str, Any]:
    """
    Analyzes Ruby code for metrics, issues, and quality assessment.
    
    This is a basic implementation for POC demonstration.
    In production, this would use proper Ruby AST parsing.
    """
    lines = code.splitlines()
    report = {
        "metrics": _calculate_metrics(lines, code),
        "issues": _detect_issues(code, lines)
    }
    return report


def _calculate_metrics(lines: List[str], code: str) -> Dict[str, Any]:
    """Calculate basic code metrics."""
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    comment_lines = [line for line in lines if line.strip().startswith('#')]
    
    # Count methods and classes
    method_count = len(re.findall(r'def\s+\w+', code))
    class_count = len(re.findall(r'class\s+\w+', code))
    
    # Calculate complexity (basic approximation)
    complexity_keywords = ['if', 'elsif', 'else', 'case', 'when', 'while', 'for', 'until']
    complexity_score = sum(code.count(keyword) for keyword in complexity_keywords))
    
    return {
        "total_lines": len(lines),
        "code_lines": len(non_empty_lines),
        "comment_lines": len(comment_lines),
        "blank_lines": len(lines) - len(non_empty_lines),
        "method_count": method_count,
        "class_count": class_count,
        "cyclomatic_complexity": complexity_score,
        "comment_ratio": round(len(comment_lines) / max(len(non_empty_lines), 1), 2)
    }


def _detect_issues(code: str, lines: List[str]) -> List[str]:
    """Detect code quality issues and anti-patterns."""
    issues = []
    
    # Security issues
    if "eval(" in code:
        issues.append("🔐 Security: Use of 'eval' is highly discouraged - potential code injection risk")
    
    if "system(" in code or "`" in code:
        issues.append("🔐 Security: System calls detected - review for command injection vulnerabilities")
    
    # Code quality issues
    if re.search(r'def\s+\w+.*\n(.*\n){20,}.*end', code, re.MULTILINE):
        issues.append("📏 Code Quality: Long method detected (>20 lines) - consider breaking into smaller methods")
    
    # Check for long lines
    long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 120]
    if long_lines:
        issues.append(f"📏 Style: Long lines detected (lines: {', '.join(map(str, long_lines[:3]))}{'...' if len(long_lines) > 3 else ''})")
    
    # Ruby-specific patterns
    if ".each do |" in code and "map" not in code:
        issues.append("♻️ Ruby Style: Consider using 'map' instead of 'each' when transforming collections")
    
    if re.search(r'if\s+.*\\.nil\\?', code):
        issues.append("♻️ Ruby Style: Consider using safe navigation operator (&.) instead of nil checks")
    
    # SOLID Principles violations (basic detection)
    if code.count("class") > 0:
        class_line_count = _estimate_class_length(code)
        if class_line_count > 50:
            issues.append("🏗️ SOLID: Large class detected - violates Single Responsibility Principle")
    
    # Magic numbers
    magic_numbers = re.findall(r'\b\d{2,}\b', code)
    if magic_numbers:
        issues.append("🔢 Code Quality: Magic numbers detected - consider using named constants")
    
    # No comments in methods
    methods = re.findall(r'def\s+(\w+).*?end', code, re.DOTALL)
    for method in methods:
        if '#' not in method:
            issues.append("📝 Documentation: Methods lacking comments detected")
            break
    
    return issues


def _estimate_class_length(code: str) -> int:
    """Estimate the length of the largest class in the code."""
    class_matches = list(re.finditer(r'class\s+\w+', code))
    if not class_matches:
        return 0
    
    max_length = 0
    for match in class_matches:
        start = match.start()
        # Find the corresponding 'end' - this is simplified
        remaining_code = code[start:]
        end_match = re.search(r'\nend\b', remaining_code)
        if end_match:
            class_code = remaining_code[:end_match.start()]
            length = len(class_code.splitlines())
            max_length = max(max_length, length)
    
    return max_length