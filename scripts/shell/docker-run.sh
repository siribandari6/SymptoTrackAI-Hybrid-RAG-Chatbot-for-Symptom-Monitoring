#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/../.."

# SymptoTrackAI - Docker Setup (Linux/Mac)
echo "========================================"
echo "SymptoTrackAI - Docker Setup"
echo "========================================"
echo

echo "Building and starting Docker containers..."
echo

docker-compose up --build -d

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Failed to start Docker containers!"
    echo "Please ensure Docker is running."
    read -p "Press enter to exit..."
    exit 1
fi

echo
echo "========================================"
echo "Docker containers started successfully!"
echo "========================================"
echo
echo "- Application URL: http://localhost:8000"
echo "- To view logs: docker-compose logs -f"
echo "- To stop: docker-compose down"
echo
echo "Opening application in browser..."
sleep 3

# Detect OS to open browser
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:8000
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
else
    echo "Automatic browser opening not supported for $OSTYPE. Please visit http://localhost:8000"
fi

read -p "Press enter to continue..."
