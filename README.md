# TDM-UI: Multi-Agent LLM Interface

TDM-UI is a modular, production-ready web application designed for enterprise-grade interaction with Large Language Models (LLMs). It features a secure, database-backed authentication layer, a premium Streamlit frontend, and a high-performance FastAPI backend.

---

## 🏗️ Architecture & Features

### 1. Premium Frontend (The Portal)
- **Technology**: Streamlit with Custom CSS.
- **Redesigned Login**: An expert-designed, centered card-based login interface for a focused user experience.
- **Session Persistence**: Conversations are saved to the backend database and tied to the user's identity.

### 2. High-Performance Backend (The Service)
- **Technology**: FastAPI (Asynchronous execution).
- **Security**: Centralized secret management and database-backed authorization.
- **Smart Launch**: The `run_app.ps1` script automatically detects and terminates orphaned processes on ports 8000 and 8501 before starting, preventing "Port in use" (Errno 10048) errors.

### 3. Scalable User Management
- **Database**: SQLite (`backend/sessions.db`) stores allowed users and chat history.
- **Management CLI**: Use `backend/user_manager.py` for administrative tasks:
  - `python user_manager.py list`: List all authorized users.
  - `python user_manager.py add <name>`: Authorize a new user.
  - `python user_manager.py bulk-add <file.txt>`: Import hundreds of users at once.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ installed and added to PATH.

### Installation & Setup
Run the setup script to create virtual environments and install dependencies:

- **Windows**: 
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\setup_env.ps1
  ```
- **macOS/Linux**: 
  ```bash
  chmod +x setup_env.sh && ./setup_env.sh
  ```

### Running the Application
Launch both services simultaneously. The Windows version includes **automatic port cleanup**.

- **Windows**: 
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\run_app.ps1
  ```
- **macOS/Linux**: 
  ```bash
  chmod +x run_app.sh && ./run_app.sh
  ```

---

## 🧪 Simulation & Testing
To verify system stability with 100+ users, use the built-in simulation tool:

1. Start the Backend.
2. Run the simulation script:
   ```powershell
   python simulate_logins.py
   ```
This will mimic 40 concurrent login requests and provide a performance report.

---

## 📂 Project Structure

```text
TDM-UI/
├── backend/            # FastAPI & AI Orchestration
│   ├── main.py         # API Gateway
│   ├── user_manager.py # Admin CLI Tool
│   └── sessions.db     # SQLite Database (Auto-created)
├── frontend/           # Streamlit UI
│   └── app.py          # Dashboard Source
├── run_app.*           # Smart execution scripts
├── setup_env.*         # Environment setup
└── simulate_logins.py  # Load testing tool
```
