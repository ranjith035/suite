# Setup Environment for TDM-UI

Write-Host "Creating Virtual Environments..." -ForegroundColor Cyan

# Backend Setup
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
deactivate
cd ..

# Frontend Setup
cd frontend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
deactivate
cd ..

Write-Host "Setup Complete. Use run_app.ps1 to start the application." -ForegroundColor Green
