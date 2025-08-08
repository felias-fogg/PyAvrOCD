#!/bin/bash
# Script to run pylint on all Python files in the project

echo "Running pylint on pyavrocd package..."
python -m pylint pyavrocd/

echo ""
echo "Running pylint on tests..."
python -m pylint tests/

echo ""
echo "Running pylint on specific files..."
python -m pylint pyavrocd/main.py pyavrocd/handler.py pyavrocd/monitor.py

echo ""
echo "Pylint analysis complete!"
