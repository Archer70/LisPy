#!/bin/bash
# LisPy Code Formatter and Linter
# Usage: scripts/format.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "Installing dev requirements..."
pip install -r requirements-dev.txt

echo "Formatting code with Black..."
python -m black lispy/ tests/ scripts/ bin/

echo "Sorting imports with isort..."
python -m isort lispy/ tests/ scripts/ bin/

echo "Running Flake8 linter..."
python -m flake8 lispy/ tests/ scripts/ bin/

echo "✅ Code formatting and linting complete!" 