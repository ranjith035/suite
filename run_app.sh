#!/bin/bash

# Run TDM-UI Services (macOS/Linux)

# Function to kill child processes on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

trap cleanup SIGINT SIGTERM

echo "Starting Backend on http://127.0.0.1:8000..."
cd backend
./venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ..

echo "Starting Frontend on http://127.0.0.1:8501..."
cd frontend
./venv/bin/python -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1 &
FRONTEND_PID=$!
cd ..

echo "------------------------------------------------"
echo "Services started."
echo "Backend: http://127.0.0.1:8000"
echo "Frontend: http://127.0.0.1:8501"
echo "Press Ctrl+C to stop both services."
echo "------------------------------------------------"

# Keep script running
wait
