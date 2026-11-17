#!/bin/bash

cd "$(dirname "$0")/../.." || exit 1

if command -v python3.12 >/dev/null 2>&1; then
    build_python=python3.12
elif command -v python3.11 >/dev/null 2>&1; then
    build_python=python3.11
else
    echo "Python 3.11 or 3.12 is required. Install one of these versions, then double-click this file again."
    read -r -p "Press Return to close this window..."
    exit 1
fi

"$build_python" packaging/build_app.py
build_status=$?
if [ "$build_status" -eq 0 ]; then
    echo "Build finished. The app is in the dist folder."
else
    echo "Build failed with exit code $build_status. Review the messages above."
fi
read -r -p "Press Return to close this window..."
exit "$build_status"
