#!/bin/bash

print_tool() {
  local name="$1"
  local purpose="$2"
  local tips="$3"
  local vuln="$4"
  local install="$5"

  echo -e "\n🔧 \033[1m$name\033[0m"
  echo "  - Purpose        : $purpose"
  echo "  - Automation Tips: $tips"
  echo "  - Vulnerabilities: $vuln"
  echo "  - Install        : $install"
}
