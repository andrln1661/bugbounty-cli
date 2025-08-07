"""
GitHub API Integration Module (Fixed)
Handles repository search, topic analysis, and database operations
"""
import os
import requests
import json
from utils.tool_utils import DB_PATH

# Configuration
GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {
    "Accept": "application/vnd.github+json",  # Updated header
    "X-GitHub-Api-Version": "2022-11-28"
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def search_repositories(keyword, per_page=10):
    """
    Search GitHub repositories by keyword (name, description, topics)
    Returns categorized tools with vulnerability analysis
    """
    # Construct search query targeting bug bounty tools
    query = f"{keyword} in:name,description,topic topic:bugbounty"
    url = f"{GITHUB_API}/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }

    print(f"🔍 Searching GitHub for: '{keyword}'...")
    resp = requests.get(url, headers=HEADERS, params=params)
    
    if resp.status_code != 200:
        print(f"❌ GitHub API error: {resp.status_code} - {resp.json().get('message')}")
        return []

    repos = resp.json().get("items", [])
    tools = []

    for repo in repos:
        # Get topics from the repository's topics_url property
        topics_url = repo.get("topics_url", "").replace("{/topic}", "")
        topics = get_repo_topics(topics_url) if topics_url else []
        
        tools.append({
            "name": repo["name"],
            "category": categorize_from_topics(topics),
            "purpose": repo["description"] or "No description",
            "automation_tips": "TBD",
            "vulnerability": extract_vulns_from_topics(topics),
            "install": repo["html_url"],
            "stars": repo["stargazers_count"]
        })

    return tools

def get_repo_topics(topics_url):
    """Fetch topics for a specific repository"""
    if not topics_url:
        return []
    
    try:
        topics_resp = requests.get(topics_url, headers=HEADERS)
        if topics_resp.status_code == 200:
            return topics_resp.json().get("names", [])
        return []
    except Exception as e:
        print(f"⚠️ Topics fetch error: {e}")
        return []
    
def categorize_from_topics(topics):
    """
    Map GitHub topics to security tool categories
    Returns 'Unknown' if no match found
    """
    CATEGORY_MAP = {
        # Web security
        "web": "Web", "web-security": "Web", "webapp": "Web",
        # Mobile security
        "mobile": "Mobile", "android": "Mobile", "ios": "Mobile",
        # Infrastructure
        "container": "Container", "docker": "Container", "kubernetes": "Container",
        # Reconnaissance
        "osint": "OSINT", "recon": "OSINT", "reconnaissance": "OSINT",
        # General security
        "bugbounty": "Bug Bounty", "security": "Security", "infosec": "Security",
        "pentesting": "Pentesting", "redteam": "Pentesting",
        # Testing techniques
        "fuzzing": "Fuzzing", "scanner": "Scanner", "vulnerability": "Scanner",
    }

    for topic in topics:
        if topic.lower() in CATEGORY_MAP:
            return CATEGORY_MAP[topic.lower()]
    return "Unknown"

def extract_vulns_from_topics(topics):
    """
    Extract vulnerability types from topic names
    Returns ['TBD'] if no vulnerabilities detected
    """
    VULN_KEYWORDS = {
        "xss", "csrf", "sqli", "sql-injection", "idor", 
        "rce", "lfi", "xxe", "ssrf", "ssti"
    }
    detected = set()
    
    for topic in topics:
        for vuln in VULN_KEYWORDS:
            if vuln in topic.lower():
                detected.add(vuln.upper())
                
    return list(detected) if detected else ["TBD"]

def save_to_db(new_tools):
    """
    Save newly discovered tools to JSON database
    Prevents duplicate entries by tool name
    """
    try:
        with open(DB_PATH, "r") as f:
            existing_tools = json.load(f)
    except FileNotFoundError:
        existing_tools = []
        
    # Deduplication
    existing_names = {t["name"].lower() for t in existing_tools}
    unique_new = [t for t in new_tools if t["name"].lower() not in existing_names]
    
    if not unique_new:
        print("⚠️ No new tools to add")
        return

    print(f"✅ Saving {len(unique_new)} new tools to database")
    updated_tools = existing_tools + unique_new
    
    with open(DB_PATH, "w") as f:
        json.dump(updated_tools, f, indent=2)