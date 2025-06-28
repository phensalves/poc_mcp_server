#!/usr/bin/env python3
"""
MCP Server CLI Tool for VS Code Integration

Usage:
    python cli.py analyze --file <file_path> --language <language> [--provider <provider>]
    python cli.py watch --directory <directory> [--provider <provider>]
    python cli.py languages
    python cli.py providers
"""

import argparse
import json
import sys
import time
import requests
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class CodeAnalysisHandler(FileSystemEventHandler):
    def __init__(self, server_url="http://localhost:8000", provider="mock"):
        self.server_url = server_url
        self.provider = provider
        self.supported_languages = self._get_supported_languages()

    def _get_supported_languages(self):
        try:
            response = requests.get(f"{self.server_url}/supported-languages")
            return response.json().get("languages", [])
        except:
            return ["python", "ruby"]  # fallback

    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix in ['.py', '.rb', '.js', '.go', '.java', '.ex']:
            self.analyze_file(file_path)

    def analyze_file(self, file_path):
        language = self._detect_language(file_path)
        if language not in self.supported_languages:
            return

        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            result = analyze_code(code, language, self.provider, self.server_url)
            if result:
                print(f"\n🔍 Analysis for {file_path}:")
                self._print_analysis(result)
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")

    def _detect_language(self, file_path):
        extension_map = {
            '.py': 'python',
            '.rb': 'ruby',
            '.js': 'javascript',
            '.go': 'go',
            '.java': 'java',
            '.ex': 'elixir'
        }
        return extension_map.get(file_path.suffix)

    def _print_analysis(self, result):
        analysis = result.get("analysis", {})
        
        # Print metrics
        metrics = analysis.get("metrics", {})
        if metrics:
            print("📊 Metrics:")
            for key, value in metrics.items():
                print(f"  • {key}: {value}")
        
        # Print issues
        issues = analysis.get("issues", [])
        if issues:
            print("⚠️  Issues:")
            for issue in issues:
                print(f"  • {issue}")
        
        # Print AI suggestion
        suggestion = analysis.get("refactoring_suggestion")
        if suggestion:
            print("🤖 AI Suggestion:")
            print(f"  {suggestion}")


def analyze_code(code, language, provider="mock", server_url="http://localhost:8000"):
    """Analyze code using the MCP server."""
    try:
        response = requests.post(
            f"{server_url}/analyze",
            json={
                "code": code,
                "language": language,
                "provider": provider
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error connecting to MCP server: {e}")
        print("💡 Make sure the server is running: docker compose up -d")
        return None


def list_languages(server_url="http://localhost:8000"):
    """List supported languages."""
    try:
        response = requests.get(f"{server_url}/supported-languages")
        response.raise_for_status()
        languages = response.json().get("languages", [])
        print("🌐 Supported Languages:")
        for lang in languages:
            print(f"  • {lang}")
    except requests.RequestException as e:
        print(f"❌ Error: {e}")


def list_providers(server_url="http://localhost:8000"):
    """List supported AI providers."""
    try:
        response = requests.get(f"{server_url}/supported-providers")
        response.raise_for_status()
        providers = response.json().get("providers", [])
        print("🤖 Supported AI Providers:")
        for provider in providers:
            print(f"  • {provider}")
    except requests.RequestException as e:
        print(f"❌ Error: {e}")


def watch_directory(directory, provider="mock", server_url="http://localhost:8000"):
    """Watch directory for file changes and analyze automatically."""
    print(f"👀 Watching {directory} for changes...")
    print("Press Ctrl+C to stop")
    
    event_handler = CodeAnalysisHandler(server_url, provider)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n✅ Stopped watching")
    observer.join()


def main():
    parser = argparse.ArgumentParser(description="MCP Server CLI Tool")
    parser.add_argument("--server", default="http://localhost:8000", 
                       help="MCP server URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a single file")
    analyze_parser.add_argument("--file", required=True, help="File to analyze")
    analyze_parser.add_argument("--language", required=True, 
                               choices=["python", "ruby", "javascript", "go", "java", "elixir"],
                               help="Programming language")
    analyze_parser.add_argument("--provider", default="mock", help="AI provider")
    
    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Watch directory for changes")
    watch_parser.add_argument("--directory", required=True, help="Directory to watch")
    watch_parser.add_argument("--provider", default="mock", help="AI provider")
    
    # List commands
    subparsers.add_parser("languages", help="List supported languages")
    subparsers.add_parser("providers", help="List supported AI providers")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "analyze":
        try:
            with open(args.file, 'r') as f:
                code = f.read()
            result = analyze_code(code, args.language, args.provider, args.server)
            if result:
                print(json.dumps(result, indent=2))
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif args.command == "watch":
        if not Path(args.directory).is_dir():
            print(f"❌ Directory not found: {args.directory}")
            return
        watch_directory(args.directory, args.provider, args.server)
    
    elif args.command == "languages":
        list_languages(args.server)
    
    elif args.command == "providers":
        list_providers(args.server)


if __name__ == "__main__":
    main()