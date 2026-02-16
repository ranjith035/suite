# Run TDM-UI Services (Direct Execution)

# Function to kill process on specific port
function Stop-PortProcess([int]$Port) {
    $processId = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -First 1
    if ($processId) {
        Write-Host "Cleaning up existing process on port $Port (PID: $processId)..." -ForegroundColor Yellow
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
}

# Cleanup ports 8000 and 8501
Stop-PortProcess 8000
Stop-PortProcess 8501

# 1. Start Backend
Write-Host "Starting Backend on http://127.0.0.1:8000..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath "backend\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000" -WorkingDirectory "backend"

# 2. Start Frontend
Write-Host "Starting Frontend on http://127.0.0.1:8501..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath "frontend\venv\Scripts\python.exe" -ArgumentList "-m", "streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "127.0.0.1" -WorkingDirectory "frontend"

Write-Host "Services started." -ForegroundColor Green
Write-Host "Backend: http://127.0.0.1:8000"
Write-Host "Frontend: http://127.0.0.1:8501"
Write-Host "Check the console for any immediate error logs." -ForegroundColor Yellow

# Keep script alive but allow output visibility
Start-Sleep -Seconds 5
