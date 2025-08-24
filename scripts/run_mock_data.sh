#!/bin/bash

echo "Running mock data generator..."

# Activate virtual environment
source .venv/bin/activate

# Run the mock data generator script
python scripts/generate_mock_data.py
