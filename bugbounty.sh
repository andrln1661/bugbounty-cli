#!/bin/bash

# Load dependencies
source utils/tool_printer.sh
source utils/tool_filter.sh

TOOL_DB="data/tools.db"

# Print help
print_help() {
  echo -e "\nUsage: $0 [options]\n"
  echo "Options:"
  echo "  -a             Show all tools"
  echo "  -n <name>      Search tool by name"
  echo "  -v <vuln>      Search by vulnerability"
  echo "  -h             Show help"
  exit 0
}

# Parse arguments
while getopts "an:v:h" opt; do
  case $opt in
    a)
      show_all_tools "$TOOL_DB"
      exit 0
      ;;
    n)
      filter_by_name "$TOOL_DB" "$OPTARG"
      exit 0
      ;;
    v)
      filter_by_vuln "$TOOL_DB" "$OPTARG"
      exit 0
      ;;
    h)
      print_help
      ;;
    *)
      echo "Invalid option. Use -h for help."
      exit 1
      ;;
  esac
done

# Default
print_help
