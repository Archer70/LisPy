#!/bin/bash
# LisPy Interpreter Launcher
# Usage: bin/lispy.sh [--repl] [file.lpy]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/lispy_interpreter.py" "$@" 