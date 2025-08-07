"""
Multi-Source Tool Search Module
Searches package repositories beyond GitHub (PyPI, Conda, npm, etc.)
"""
import os
import subprocess
import xmlrpc.client
import requests
from utils.github_api import search_repositories

# Configuration
PYPI_URL = "https://pypi.org/pypi"
CONDA_URL = "https://api.anaconda.org/search"
NPM_URL = "https://registry.npmjs.org/-/v1/search"

def pypi_search(keyword, limit=5):
    """Search Python Package Index (PyPI) for security tools"""
    try:
        client = xmlrpc.client.ServerProxy(PYPI_URL)
        results = client.search({'name': keyword}, 'or')[:limit]
        return [{
            "name": pkg['name'],
            "category": "Python",
            "purpose": pkg.get('summary', 'No description'),
            "automation_tips": f"pip install {pkg['name']}",
            "vulnerability": ["TBD"],
            "install": f"pip install {pkg['name']}",
            "stars": 0  # PyPI doesn't have star ratings
        } for pkg in results]
    except Exception as e:
        print(f"❌ PyPI error: {e}")
        return []

def conda_search(keyword, limit=5):
    """Search Anaconda repositories for security tools"""
    try:
        params = {'q': keyword, 'limit': limit}
        resp = requests.get(CONDA_URL, params=params, timeout=10)
        return [{
            "name": pkg['full_name'],
            "category": "Conda",
            "purpose": pkg.get('summary', 'No description'),
            "automation_tips": f"conda install {pkg['full_name']}",
            "vulnerability": ["TBD"],
            "install": f"conda install {pkg['full_name']}",
            "stars": 0
        } for pkg in resp.json()] if resp.status_code == 200 else []
    except Exception as e:
        print(f"❌ Conda error: {e}")
        return []

def npm_search(keyword, limit=5):
    """Search npm registry for security tools"""
    try:
        params = {'text': keyword, 'size': limit}
        resp = requests.get(NPM_URL, params=params, timeout=10)
        return [{
            "name": pkg['package']['name'],
            "category": "npm",
            "purpose": pkg['package'].get('description', 'No description'),
            "automation_tips": f"npm install {pkg['package']['name']}",
            "vulnerability": ["TBD"],
            "install": f"npm install {pkg['package']['name']}",
            "stars": 0
        } for pkg in resp.json().get('objects', [])] if resp.status_code == 200 else []
    except Exception as e:
        print(f"❌ npm error: {e}")
        return []

def linux_pkg_search(keyword, limit=5):
    """Search Linux package repositories (apt) for security tools"""
    try:
        result = subprocess.run(
            ['apt-cache', 'search', keyword],
            capture_output=True,
            text=True,
            timeout=10
        )
        packages = result.stdout.splitlines()[:limit]
        return [{
            "name": pkg.split(' - ')[0],
            "category": "Linux",
            "purpose": pkg.split(' - ')[1] if ' - ' in pkg else 'No description',
            "automation_tips": f"sudo apt install {pkg.split(' - ')[0]}",
            "vulnerability": ["TBD"],
            "install": f"sudo apt install {pkg.split(' - ')[0]}",
            "stars": 0
        } for pkg in packages]
    except Exception as e:
        print(f"❌ Linux package error: {e}")
        return []

def search_all_sources(keyword, limit=5):
    """
    Aggregate search across all available sources
    Returns unified, deduplicated list of tools sorted by popularity
    """
    sources = [
        search_repositories(keyword, limit),  # GitHub
        pypi_search(keyword, limit),
        conda_search(keyword, limit),
        npm_search(keyword, limit),
        linux_pkg_search(keyword, limit)
    ]
    
    # Flatten and deduplicate results
    all_tools = []
    seen_names = set()
    
    for source in sources:
        for tool in source:
            if tool['name'] not in seen_names:
                all_tools.append(tool)
                seen_names.add(tool['name'])
    
    # Sort by stars (GitHub) descending, others come last
    all_tools.sort(key=lambda x: x.get('stars', 0), reverse=True)
    return all_tools

def filter_tools(tools, name=None, vuln=None):
    """Filter tools by name and vulnerability type"""
    filtered = tools
    if name:
        filtered = [t for t in filtered if name.lower() in t['name'].lower()]
    if vuln:
        filtered = [t for t in filtered if any(vuln.lower() in v.lower() for v in t['vulnerability'])]
    return filtered