#!/bin/bash
# Check pod memory usage vs limits, alert if any pod exceeds 60%

export AWS_ACCESS_KEY_ID=AKIAZZDPA5LKS7MH6C24
export AWS_SECRET_ACCESS_KEY=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
export PATH="/workspace:/workspace/.local/bin:$PATH"

THRESHOLD=60
ALERTS=""

# Get all pods with their memory usage (in Mi)
while IFS= read -r line; do
  NAMESPACE=$(echo "$line" | awk '{print $1}')
  POD=$(echo "$line" | awk '{print $2}')
  MEM_USAGE=$(echo "$line" | awk '{print $4}' | sed 's/Mi//')

  # Skip header
  [[ "$POD" == "NAME" ]] && continue
  [[ -z "$MEM_USAGE" || "$MEM_USAGE" == "0" ]] && continue

  # Get memory limit for this pod
  MEM_LIMIT=$(/workspace/kubectl get pod "$POD" -n "$NAMESPACE" \
    -o jsonpath='{.spec.containers[0].resources.limits.memory}' 2>/dev/null)

  if [[ -z "$MEM_LIMIT" ]]; then
    continue  # No limit set, skip
  fi

  # Convert limit to Mi
  if [[ "$MEM_LIMIT" == *Gi ]]; then
    LIMIT_MI=$(echo "$MEM_LIMIT" | sed 's/Gi//' | awk '{print $1 * 1024}')
  elif [[ "$MEM_LIMIT" == *Mi ]]; then
    LIMIT_MI=$(echo "$MEM_LIMIT" | sed 's/Mi//')
  elif [[ "$MEM_LIMIT" == *Ki ]]; then
    LIMIT_MI=$(echo "$MEM_LIMIT" | sed 's/Ki//' | awk '{print $1 / 1024}')
  else
    continue
  fi

  # Calculate percentage
  if [[ "$LIMIT_MI" -gt 0 ]]; then
    PCT=$(awk "BEGIN {printf \"%.0f\", ($MEM_USAGE / $LIMIT_MI) * 100}")
    if [[ "$PCT" -ge "$THRESHOLD" ]]; then
      ALERTS="$ALERTS\n⚠️ $NAMESPACE/$POD: ${MEM_USAGE}Mi / ${LIMIT_MI}Mi (${PCT}%)"
    fi
  fi

done < <(/workspace/kubectl top pods --all-namespaces --no-headers 2>/dev/null)

if [[ -n "$ALERTS" ]]; then
  echo "🚨 Pod memory usage >= ${THRESHOLD}%:"
  echo -e "$ALERTS"
else
  echo "OK: No pods exceeding ${THRESHOLD}% memory usage"
fi
