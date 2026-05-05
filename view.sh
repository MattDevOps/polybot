#!/usr/bin/env bash
# Serve the dashboard locally at http://localhost:8000/dashboard.html
set -euo pipefail

cd "$(dirname "$0")/reports"

if [ ! -f dashboard.html ]; then
    cp ../dashboard_triple.html dashboard.html
fi

echo "Dashboard: http://localhost:8000/dashboard.html"
echo "Ctrl+C to stop."
xdg-open http://localhost:8000/dashboard.html >/dev/null 2>&1 &
exec python3 -m http.server 8000
