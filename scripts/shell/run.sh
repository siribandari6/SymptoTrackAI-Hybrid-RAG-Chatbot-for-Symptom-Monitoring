#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/../.."

# SymptoTrackAI - Run Server (Linux/Mac)
# Ensure virtual environment is activated before running this
python manage.py runserver --noreload

read -p "Press enter to continue..."
