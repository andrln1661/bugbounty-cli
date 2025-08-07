#!/bin/bash

source utils/tool_printer.sh

show_all_tools() {
  local db="$1"
  while IFS='|' read -r name purpose tips vuln install; do
    print_tool "$name" "$purpose" "$tips" "$vuln" "$install"
  done < "$db"
}

filter_by_name() {
  local db="$1"
  local query=$(echo "$2" | tr '[:upper:]' '[:lower:]')
  local found=false
  while IFS='|' read -r name purpose tips vuln install; do
    lname=$(echo "$name" | tr '[:upper:]' '[:lower:]')
    if [[ "$lname" == *"$query"* ]]; then
      print_tool "$name" "$purpose" "$tips" "$vuln" "$install"
      found=true
    fi
  done < "$db"
  $found || echo "No tool found matching name '$query'"
}

filter_by_vuln() {
  local db="$1"
  local query=$(echo "$2" | tr '[:upper:]' '[:lower:]')
  local found=false
  while IFS='|' read -r name purpose tips vuln install; do
    lvuln=$(echo "$vuln" | tr '[:upper:]' '[:lower:]')
    if [[ "$lvuln" == *"$query"* ]]; then
      print_tool "$name" "$purpose" "$tips" "$vuln" "$install"
      found=true
    fi
  done < "$db"
  $found || echo "No tool found matching vulnerability '$query'"
}
