#!/bin/bash
# LisPy Test Suite Runner
# Usage: scripts/test.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."
python3 -m unittest discover -s tests -p "*_test.py" 