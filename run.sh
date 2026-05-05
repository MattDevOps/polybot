#!/usr/bin/env bash
# Linux equivalent of LAUNCH_SINGLE.bat — runs the alpha bot once.
# For cron use. Outputs reports/latest_report.json (and serious_latest.json, original_latest.json).
set -euo pipefail

cd "$(dirname "$0")"

if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

if [ -z "${PERPLEXITY_API_KEY:-}" ]; then
    echo "WARNING: PERPLEXITY_API_KEY not set — bot will fall back to basic analysis."
    echo "  export PERPLEXITY_API_KEY='your-key' (add to ~/.bashrc to persist)"
fi

PY="${PYTHON:-python3}"
"$PY" polymarket_alpha_bot.py

cp -f dashboard_triple.html reports/dashboard.html 2>/dev/null || true
echo "Done. View dashboard with: ./view.sh"
