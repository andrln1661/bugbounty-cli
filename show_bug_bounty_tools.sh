#!/bin/bash

# Define tool list as an array of strings
tools=(
"Burp Suite|Web vulnerability scanner and proxy|Use Burp Extensions|XSS, SQLi, CSRF|https://portswigger.net/burp"
"Nmap|Network scanning and discovery|Use with NSE scripts|Open ports|sudo apt install nmap"
"Amass|Subdomain enumeration|Automate with cron|Subdomain takeover|sudo snap install amass"
"SQLmap|SQL injection tool|Run in batch mode|SQLi|sudo apt install sqlmap"
"Dirb|Brute-force directories|Custom wordlists|Hidden paths|sudo apt install dirb"
"ffuf|Web fuzzing|CI/recon JSON output|Path fuzzing|go install github.com/ffuf/ffuf/v2@latest"
"Nikto|Web server scanner|Cron jobs|Outdated software|sudo apt install nikto"
"MobSF|Mobile app analysis|API integration|Insecure storage|https://github.com/MobSF/Mobile-Security-Framework-MobSF"
"Frida|Runtime instrumentation|Python scripts|Runtime hacking|pip install frida-tools"
"Trivy|Container scanning|CI/CD integration|CVE, misconfig|brew install trivy"
"SpiderFoot|Automated OSINT|CLI/API mode|Metadata leaks|https://github.com/smicallef/spiderfoot"
)

# Help function
print_help() {
  echo -e "Bug bounty tools cheatsheet"  
  echo -e "Usage: $0 [options]\n"
  echo "Options:"
  echo "  -a             Show all tools"
  echo "  -n <name>      Search tool by name"
  echo "  -v <vuln>      Search tool by vulnerability type"
  echo "  -h             Show this message"
  exit 0
}

# Print tool entry
print_tool() {
  IFS='|' read -r name purpose tips vuln install <<< "$1"
  echo -e "🔧 \033[1m$name\033[0m"
  echo -e "  - \033[1mPurpose:\033[0m $purpose"
  echo -e "  - \033[1mAutomation Tips:\033[0m $tips"
  echo -e "  - \033[1mVulnerabilities:\033[0m $vuln"
  echo -e "  - \033[1mInstall:\033[0m $install"
  echo ""
}

# Parse options
while getopts "an:v:h" opt; do
  case $opt in
    a)
      for tool in "${tools[@]}"; do
        print_tool "$tool"
      done
      exit 0
      ;;
    n)
      query=$(echo "$OPTARG" | tr '[:upper:]' '[:lower:]')
      found=false
      for tool in "${tools[@]}"; do
        name=$(echo "$tool" | cut -d'|' -f1 | tr '[:upper:]' '[:lower:]')
        if [[ "$name" == *"$query"* ]]; then
          print_tool "$tool"
          found=true
        fi
      done
      $found || echo "No tool found with name matching '$query'"
      exit 0
      ;;
    v)
      query=$(echo "$OPTARG" | tr '[:upper:]' '[:lower:]')
      found=false
      for tool in "${tools[@]}"; do
        vuln=$(echo "$tool" | cut -d'|' -f4 | tr '[:upper:]' '[:lower:]')
        if [[ "$vuln" == *"$query"* ]]; then
          print_tool "$tool"
          found=true
        fi
      done
      $found || echo "No tool found targeting vulnerability type '$query'"
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

# Default to help if no options given
print_help
