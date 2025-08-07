#!/usr/bin/env python3
"""
🔧 Main CLI for Bug Bounty Tool Finder
Handles command-line arguments and orchestrates tool search operations
"""
import argparse
from utils.tool_utils import load_tools, print_tool
from utils.multi_source_search import search_all_sources, filter_tools
from utils.github_api import search_repositories, save_to_db

def main():
    parser = argparse.ArgumentParser(
        description="🔧 Bug Bounty Tool Finder - Discover security tools across multiple sources",
        epilog="Example: ./main.py --search-all xss --filter-vuln xss"
    )
    # Search arguments
    parser.add_argument(
        "-s", "--search-all", metavar="KEYWORD",
        help="Search across GitHub, PyPI, Conda, npm, Linux packages"
    )
    parser.add_argument(
        "--search-gh", metavar="KEYWORD", 
        help="Search GitHub repositories only"
    )
    
    # Filter arguments
    parser.add_argument(
        "-fn", "--filter-name", metavar="NAME",
        help="Filter results by tool name"
    )
    parser.add_argument(
        "-fv", "--filter-vuln", metavar="VULN",
        help="Filter results by vulnerability type"
    )
    parser.add_argument(
        "-c", "--category", metavar="CATEGORY",
        help="Filter by category (Web, Mobile, Container, etc.)"
    )
    
    # Database operations
    parser.add_argument(
        "--sync-gh", metavar="KEYWORD", 
        help="Search GitHub and save new tools to local DB"
    )
    parser.add_argument(
        "-a", "--all", action="store_true",
        help="Show all tools in local database"
    )
    
    args = parser.parse_args()
    tools = load_tools()

    # Command routing
    if args.search_all:
        results = search_all_sources(args.search_all, limit=15)
        results = filter_tools(results, args.filter_name, args.filter_vuln)
        if args.category:
            results = [t for t in results if t['category'].lower() == args.category.lower()]
        for tool in results:
            print_tool(tool)
            
    elif args.search_gh:
        results = search_repositories(args.search_gh, per_page=10)
        for tool in results:
            print_tool(tool)
            
    elif args.sync_gh:
        new_tools = search_repositories(args.sync_gh, per_page=20)
        save_to_db(new_tools)
        print(f"Synced {len(new_tools)} tools to database")
        
    elif args.all:
        for tool in tools:
            print_tool(tool)
            
    elif args.filter_name or args.filter_vuln or args.category:
        results = tools
        if args.filter_name:
            results = [t for t in results if args.filter_name.lower() in t['name'].lower()]
        if args.filter_vuln:
            results = [t for t in results if any(args.filter_vuln.lower() in v.lower() for v in t['vulnerability'])]
        if args.category:
            results = [t for t in results if args.category.lower() == t['category'].lower()]
        for tool in results:
            print_tool(tool)
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()