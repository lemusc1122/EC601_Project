#!/usr/bin/env bash
set -Eeuo pipefail

# Install the project's Python dependencies into a local virtual environment.
# Run from the folder where you want the .venv directory created.

VENV_DIR="${VENV_DIR:-.venv}"
PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Error: $PYTHON was not found. Install Python 3 and try again." >&2
    exit 1
fi

echo "Using Python:"
"$PYTHON" --version

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    echo "Creating virtual environment at: $VENV_DIR"
    "$PYTHON" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing dependencies..."
python -m pip install \
    "PySide6" \
    "numpy==1.26.4" \
    "qiskit==2.4.2" \
    "matplotlib"

echo
echo "Checking installed packages..."
python - <<'PY'
from importlib.metadata import version

packages = ("PySide6", "numpy", "qiskit", "matplotlib")
for package in packages:
    print(f"{package}=={version(package)}")

import numpy
import qiskit
import matplotlib
from PySide6 import QtCore

print("\nImport checks passed.")
print(f"Qt version: {QtCore.qVersion()}")
PY

echo
echo "Installation complete."
echo "To activate this environment in a new terminal, run:"
echo "  source \"$VENV_DIR/bin/activate\""
echo "Then launch your program using:"
echo "  python your_script.py"
