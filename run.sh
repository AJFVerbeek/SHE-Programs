#!/usr/bin/env bash
# Start de SHE-Programs-applicatie.
#
# Gebruik:
#   ./run.sh            # start de app (http://127.0.0.1:8000)
#   HOST=0.0.0.0 PORT=9000 ./run.sh   # eigen host/poort
#
# Het script maakt eenmalig een virtuele omgeving aan (.venv) en
# installeert de dependencies; daarna start het de webserver.

set -euo pipefail

# Ga naar de map waarin dit script staat (de projectroot).
cd "$(dirname "$0")"

VENV_DIR=".venv"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

# 1. Virtuele omgeving aanmaken indien die nog niet bestaat.
if [ ! -d "$VENV_DIR" ]; then
    echo "==> Virtuele omgeving aanmaken in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# 2. Activeren.
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# 3. Dependencies installeren (idempotent; pip slaat reeds geïnstalleerde over).
echo "==> Dependencies installeren"
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# 4. App starten.
echo "==> Server starten op http://$HOST:$PORT"
echo "    RI&E:        http://$HOST:$PORT/"
echo "    Incidenten:  http://$HOST:$PORT/incidents"
echo "    API-docs:    http://$HOST:$PORT/docs"
echo "    (stoppen met Ctrl+C)"
exec uvicorn app.main:app --reload --host "$HOST" --port "$PORT"
