#!/bin/bash

# Exit on error
set -e

PYTHON_VERSION=3.9.18

echo "Installing Python $PYTHON_VERSION via pyenv..."
pyenv install -s $PYTHON_VERSION
pyenv local $PYTHON_VERSION

echo "Creating virtual environment (.venv)..."
python -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Use 'source .venv/bin/activate' to activate the environment."
