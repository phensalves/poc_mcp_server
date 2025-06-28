# VS Code Integration Guide

This guide shows how to integrate the MCP Server with Visual Studio Code for real-time code analysis and AI-powered suggestions.

## Quick Start (5 minutes)

### 1. Start the MCP Server
```bash
# Clone and start the server
git clone <repository-url>
cd mcp_server
docker compose up -d

# Verify it's running
curl http://localhost:8000/supported-languages
```

### 2. Install CLI Dependencies
```bash
# Install Python dependencies for the CLI tool
pip install -r cli-requirements.txt
```

### 3. Test the CLI Tool
```bash
# Analyze a single file
python cli.py analyze --file app/main.py --language python

# List supported languages and providers
python cli.py languages
python cli.py providers
```

### 4. Set Up VS Code Integration

#### Option A: Manual Analysis (Immediate)
Create a VS Code task for manual analysis:

1. Open VS Code in your project directory
2. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
3. Type "Tasks: Configure Task" and select it
4. Add this configuration to `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "MCP Analyze Current File",
            "type": "shell",
            "command": "python",
            "args": [
                "/path/to/mcp_server/cli.py",
                "analyze",
                "--file",
                "${file}",
                "--language",
                "${input:language}",
                "--provider",
                "mock"
            ],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        }
    ],
    "inputs": [
        {
            "id": "language",
            "description": "Programming Language",
            "default": "python",
            "type": "pickString",
            "options": [
                "python",
                "ruby",
                "javascript",
                "go",
                "java",
                "elixir"
            ]
        }
    ]
}
```

5. Press `Ctrl+Shift+P` and run "Tasks: Run Task" → "MCP Analyze Current File"

#### Option B: Real-time Watching (Recommended)
Set up automatic file watching:

1. Open terminal in VS Code (`Ctrl+``)
2. Run the watcher:
```bash
python /path/to/mcp_server/cli.py watch --directory . --provider mock
```

This will automatically analyze files when you save them.

#### Option C: Keyboard Shortcut
Add this to your VS Code `keybindings.json`:

```json
[
    {
        "key": "ctrl+shift+a",
        "command": "workbench.action.tasks.runTask",
        "args": "MCP Analyze Current File"
    }
]
```

## Advanced Configuration

### Custom Settings
Create a `.mcp-config.json` in your project root:

```json
{
    "server_url": "http://localhost:8000",
    "default_provider": "mock",
    "auto_analyze": true,
    "languages": {
        "python": {
            "provider": "openai",
            "max_line_length": 88
        },
        "ruby": {
            "provider": "mock",
            "max_line_length": 120
        }
    },
    "ignore_patterns": [
        "node_modules/*",
        "venv/*",
        ".git/*",
        "*.min.js"
    ]
}
```

### AI Provider Setup

#### OpenAI Integration
1. Get your API key from https://platform.openai.com/
2. Set environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```
3. Restart the Docker services:
```bash
docker compose down
docker compose up -d
```

#### Mock Provider (Default)
No setup required. Provides realistic suggestions for testing.

## Usage Examples

### Single File Analysis
```bash
# Analyze a Ruby file
python cli.py analyze --file app/models/user.rb --language ruby

# Analyze with OpenAI
python cli.py analyze --file app/main.py --language python --provider openai
```

### Project Monitoring
```bash
# Watch entire project
python cli.py watch --directory . --provider mock

# Watch specific subdirectory
python cli.py watch --directory app/ --provider openai
```

### Output Examples

#### Ruby Analysis Result:
```json
{
  "language": "ruby",
  "analysis": {
    "metrics": {
      "total_lines": 45,
      "code_lines": 38,
      "comment_lines": 3,
      "method_count": 4,
      "class_count": 1,
      "cyclomatic_complexity": 6,
      "comment_ratio": 0.08
    },
    "issues": [
      "🔐 Security: Use of 'eval' is highly discouraged - potential code injection risk",
      "📏 Code Quality: Long method detected (>20 lines) - consider breaking into smaller methods",
      "♻️ Ruby Style: Consider using 'map' instead of 'each' when transforming collections"
    ],
    "refactoring_suggestion": "[Mock Suggestion] Consider simplifying the following code..."
  }
}
```

## Troubleshooting

### Common Issues

**1. "Connection refused" error**
```bash
# Check if server is running
docker compose ps
# If not running, start it
docker compose up -d
```

**2. "Command not found: python"**
```bash
# Try with python3
python3 cli.py analyze --file app/main.py --language python
```

**3. "Module not found" error**
```bash
# Install dependencies
pip install -r cli-requirements.txt
```

**4. File not being analyzed automatically**
- Check that the file extension is supported (.py, .rb, .js, .go, .java, .ex)
- Verify the server is responding: `curl http://localhost:8000/supported-languages`

### Performance Tips

1. **Exclude large directories** from watching:
   ```bash
   # Don't watch node_modules, venv, etc.
   python cli.py watch --directory src/ --provider mock
   ```

2. **Use specific language analyzers** for better performance:
   ```bash
   # Instead of auto-detection, specify language
   python cli.py analyze --file script.py --language python
   ```

3. **Batch analysis** for large codebases:
   ```bash
   # Analyze multiple files
   find . -name "*.py" -exec python cli.py analyze --file {} --language python \;
   ```

## Next Steps

1. **Install Real AI Providers**: Set up OpenAI or Anthropic API keys
2. **Add More Languages**: Extend support for your tech stack
3. **Custom Rules**: Configure project-specific analysis rules
4. **Team Integration**: Share configuration across your team
5. **CI/CD Integration**: Add to your deployment pipeline

## Feedback and Issues

For issues or feature requests, please check the project's GitHub repository or contact the development team.