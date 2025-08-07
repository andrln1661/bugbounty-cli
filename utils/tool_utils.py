"""
Tool Database Utilities
Handles tool storage, retrieval, and presentation
"""
import os
import json

# Path configuration
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "tools.json")

# Ensure data directory exists
os.makedirs(DB_DIR, exist_ok=True)

def load_tools():
    """Load tools from JSON database, return empty list if not found"""
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def print_tool(tool):
    """Print formatted tool information to console"""
    print(f"\n🔧 \033[1m{tool['name']}\033[0m [\033[32m{tool['category']}\033[0m]")
    print(f"  📝 Purpose: {tool['purpose']}")
    print(f"  🤖 Automation: {tool['automation_tips']}")
    print(f"  🎯 Vulnerabilities: {', '.join(tool['vulnerability'])}")
    print(f"  📦 Install: {tool['install']}")
    if tool.get('stars', 0) > 0:
        print(f"  ⭐ Stars: {tool['stars']}")

def filter_by_name(tools, query):
    """Filter tools by name substring match (case-insensitive)"""
    return [t for t in tools if query.lower() in t['name'].lower()]

def filter_by_vuln(tools, query):
    """Filter tools by vulnerability substring match (case-insensitive)"""
    return [t for t in tools if any(query.lower() in v.lower() for v in t['vulnerability'])]

def filter_by_category(tools, query):
    """Filter tools by exact category match (case-insensitive)"""
    return [t for t in tools if query.lower() == t['category'].lower()]