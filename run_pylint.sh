#!/bin/bash
# Script to run pylint on all Python files in the project

echo "Running pylint on pyavrocd package..."
python3 -m pylint pyavrocd/

echo ""
echo "Running pylint on tests..."
python3 -m pylint tests/

echo ""
echo "Pylint analysis complete!"
