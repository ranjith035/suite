#!/bin/bash

# Setup Environment for TDM-UI (macOS/Linux)

echo "Creating Virtual Environments..."

# Backend Setup
echo "--- Setting up Backend ---"
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

# Frontend Setup
echo "--- Setting up Frontend ---"
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

echo "------------------------------------------------"
echo "Setup Complete. Use ./run_app.sh to start the application."
echo "Note: You might need to make scripts executable first:"
echo "chmod +x setup_env.sh run_app.sh"
