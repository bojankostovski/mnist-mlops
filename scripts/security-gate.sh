#!/bin/bash
set -e

echo "🔒 Running Security Gate Checks..."

FAILED=0

# 1. Check Semgrep results
echo "📝 Checking SAST results..."
SEMGREP_FINDINGS=$(semgrep --config=auto . --json | jq '.results | length')
if [ "$SEMGREP_FINDINGS" -gt 0 ]; then
    echo "❌ Found $SEMGREP_FINDINGS code security issues"
    FAILED=1
else
    echo "✅ No code security issues found"
fi

# 2. Check Trivy results
echo "🐳 Checking container vulnerabilities..."
TRIVY_CRITICAL=$(trivy image --format json --severity CRITICAL mnist-torchserve:latest | jq '.Results[].Vulnerabilities | length')
TRIVY_HIGH=$(trivy image --format json --severity HIGH mnist-torchserve:latest | jq '.Results[].Vulnerabilities | length')

if [ "$TRIVY_CRITICAL" -gt 0 ]; then
    echo "❌ Found $TRIVY_CRITICAL CRITICAL vulnerabilities"
    FAILED=1
fi

if [ "$TRIVY_HIGH" -gt 10 ]; then
    echo "⚠️  Found $TRIVY_HIGH HIGH vulnerabilities (threshold: 10)"
    FAILED=1
fi

# 3. Check Gitleaks results
echo "🔑 Checking for secrets..."
if gitleaks detect --no-git; then
    echo "✅ No secrets found"
else
    echo "❌ Secrets detected!"
    FAILED=1
fi

# 4. Check Safety results
echo "📦 Checking Python dependencies..."
SAFETY_CRITICAL=$(python3 -m safety check --json | jq '[.vulnerabilities[] | select(.severity == "critical")] | length')
if [ "$SAFETY_CRITICAL" -gt 0 ]; then
    echo "❌ Found $SAFETY_CRITICAL critical vulnerabilities in dependencies"
    FAILED=1
else
    echo "✅ No critical dependency vulnerabilities"
fi

# Final result
echo ""
if [ $FAILED -eq 1 ]; then
    echo "❌ Security gate FAILED - blocking deployment"
    exit 1
else
    echo "✅ Security gate PASSED - deployment allowed"
    exit 0
fi