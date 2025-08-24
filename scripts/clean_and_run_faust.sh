#!/bin/bash

echo "Cleaning Faust cache and temp files..."

# Remove Faust cache, pycache, and temp folders
rm -rf .faust
rm -rf __pycache__/
rm -rf */__pycache__/
rm -rf ./thmanyah-streaming-*

echo "Cleanup complete."

# Activate virtual environment and run Faust
echo "Starting Faust app..."
source .venv/bin/activate && \
faust -A app.faust_app worker -l info
