#!/usr/bin/env bash
set -euo pipefail

# Determine the directory containing this script (resolves symlinks)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Paths for venv and script
VENV_DIR="$SCRIPT_DIR/venv"
ACTIVATE="$VENV_DIR/bin/activate"
PY_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"
PY_SCRIPT="$SCRIPT_DIR/bibleverse.py"

# # Create virtualenv if missing
# if [ ! -d "$VENV_DIR" ]; then
#     echo "Creating virtual environment in $VENV_DIR..."
#     python3 -m venv "$VENV_DIR"
# fi

# # Activate venv if possible (sourced into this shell); if not, we'll call the venv python directly.
# if [ -f "$ACTIVATE" ]; then
#     # shellcheck disable=SC1091
#     source "$ACTIVATE"
# else
#     echo "Warning: activate script not found; using venv python directly: $PY_BIN"
# fi

# # Ensure pip is available and upgrade quietly
# if [ -x "$PIP_BIN" ]; then
#     "$PIP_BIN" install --upgrade pip -q || true
# fi

# # Install requirements if present
# if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
#     if [ -x "$PIP_BIN" ]; then
#         "$PIP_BIN" install -r "$SCRIPT_DIR/requirements.txt" -q
#     else
#         echo "pip not found in venv; attempting to use system pip to install requirements"
#         pip install -r "$SCRIPT_DIR/requirements.txt" -q || true
#     fi
# fi

# Execute the Python script with venv python so this works regardless of PWD
# exec "$PY_BIN" "$PY_SCRIPT" "$@"
exec "$PY_SCRIPT" "$@"