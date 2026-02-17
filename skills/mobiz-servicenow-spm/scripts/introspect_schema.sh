#!/bin/bash
# ServiceNow SPM Schema Introspection Script
# Queries the AI Bridge for table metadata and outputs markdown
#
# Usage: ./introspect_schema.sh <instance_url> <username> <password>
# Example: ./introspect_schema.sh https://devXXXXXX.service-now.com admin password123
#
# Output: Markdown to stdout (redirect to references/instance-schema.md)

set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: $0 <instance_url> <username> <password>"
  echo "Example: $0 https://devXXXXXX.service-now.com admin password123"
  exit 1
fi

INSTANCE="$1"
USER="$2"
PASS="$3"
BASE_URL="$INSTANCE/api/1851835/ai_adapter_rest"

# Core SPM tables to introspect
SPM_TABLES=(
  "pm_project"
  "pm_project_task"
  "pm_milestone"
  "pm_portfolio"
  "pm_program"
  "rm_epic"
  "rm_story"
  "rm_sprint"
  "rm_defect"
  "rm_scrum_task"
  "resource_plan"
  "resource_allocation"
  "time_card"
  "time_sheet"
  "dmn_demand"
  "cost_plan"
  "planned_task_rel_planned_task"
)

echo "# Instance Schema: $(echo "$INSTANCE" | sed 's|https://||')"
echo ""
echo "Generated: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo ""
echo "---"
echo ""

# Test connectivity first
echo "## Connectivity Test"
echo ""
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -u "$USER:$PASS" "$BASE_URL/pm_project?sysparm_limit=1")
if [ "$HTTP_CODE" = "200" ]; then
  echo "Connection successful (HTTP $HTTP_CODE)"
else
  echo "Connection FAILED (HTTP $HTTP_CODE). Check credentials and AI Bridge installation."
  exit 1
fi
echo ""
echo "---"
echo ""

# Introspect each table
for TABLE in "${SPM_TABLES[@]}"; do
  echo "## $TABLE"
  echo ""

  # Check if table exists by querying 1 record
  RESULT=$(curl -s -u "$USER:$PASS" "$BASE_URL/$TABLE?sysparm_limit=1" 2>/dev/null)
  if echo "$RESULT" | jq -e '.result.error // .error' > /dev/null 2>&1; then
    echo "**Table not accessible** (may require plugin activation)"
    echo ""
    echo "---"
    echo ""
    continue
  fi

  # Get field definitions from sys_dictionary
  echo "### Fields"
  echo ""
  echo "| Field | Label | Type | Mandatory | Max Length | Reference |"
  echo "|-------|-------|------|-----------|-----------|-----------|"

  FIELDS=$(curl -s -u "$USER:$PASS" \
    "$BASE_URL/sys_dictionary?sysparm_query=name=$TABLE^elementISNOTEMPTY^active=true&sysparm_fields=element,column_label,internal_type,mandatory,max_length,reference&sysparm_display_value=true&sysparm_limit=200" 2>/dev/null)

  echo "$FIELDS" | jq -r '.result.result[]? | "| \(.element // "-") | \(.column_label // "-") | \(.internal_type // "-") | \(.mandatory // "false") | \(.max_length // "-") | \(.reference // "-") |"' 2>/dev/null || echo "| (could not retrieve fields) | | | | | |"

  echo ""

  # Get choice values for this table
  CHOICES=$(curl -s -u "$USER:$PASS" \
    "$BASE_URL/sys_choice?sysparm_query=name=$TABLE&sysparm_fields=element,label,value&sysparm_display_value=true&sysparm_limit=200" 2>/dev/null)

  CHOICE_COUNT=$(echo "$CHOICES" | jq '.result.result | length' 2>/dev/null || echo "0")
  if [ "$CHOICE_COUNT" -gt 0 ] 2>/dev/null; then
    echo "### Choice Values"
    echo ""
    echo "| Field | Value | Label |"
    echo "|-------|-------|-------|"
    echo "$CHOICES" | jq -r '.result.result[]? | "| \(.element // "-") | \(.value // "-") | \(.label // "-") |"' 2>/dev/null || true
    echo ""
  fi

  echo "---"
  echo ""
done

# Get key users
echo "## Key Users"
echo ""
echo "| sys_id | Name | Email | Title |"
echo "|--------|------|-------|-------|"

USERS=$(curl -s -u "$USER:$PASS" \
  "$BASE_URL/sys_user?sysparm_query=active=true&sysparm_fields=sys_id,name,email,title&sysparm_limit=200&sysparm_display_value=true" 2>/dev/null)

echo "$USERS" | jq -r '.result.result[]? | "| \(.sys_id // "-") | \(.name // "-") | \(.email // "-") | \(.title // "-") |"' 2>/dev/null || echo "| (could not retrieve users) | | | |"

echo ""
echo "---"
echo ""
echo "*End of schema introspection*"
