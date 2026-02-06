#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/../.."

# SymptoTrackAI - Setup and Run (Linux/Mac)
echo "========================================"
echo "SymptoTrackAI - Setup and Run"
echo "========================================"
echo

# Activate the virtual environment using UV
echo "[1/3] Activating virtual environment (UV with Python 3.8.10)..."
if [ -f "my-project/bin/activate" ]; then
    source my-project/bin/activate
    echo "Virtual environment activated successfully!"
else
    echo "ERROR: Virtual environment not found!"
    echo "Creating virtual environment using UV with Python 3.8.10..."
    uv venv my-project --python 3.8.10
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment!"
        echo "Please ensure UV is installed and Python 3.8.10 is available"
        read -p "Press enter to exit..."
        exit 1
    fi
    source my-project/bin/activate
    echo "Virtual environment created and activated!"
fi
echo

# Install requirements using UV
echo "[2/3] Installing dependencies from requirements.txt using UV..."
if [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install requirements!"
        read -p "Press enter to exit..."
        exit 1
    fi
    echo "Dependencies installed successfully!"
else
    echo "WARNING: requirements.txt not found, skipping installation..."
fi
echo

# Run the Django server
echo "[3/3] Starting Django development server..."
echo
python manage.py runserver --noreload

# Keep terminal open if run manually
read -p "Press enter to continue..."
