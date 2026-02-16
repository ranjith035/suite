# TDM-UI: Multi-Agent LLM Interface

TDM-UI is a modular web application designed to provide a persistent, multi-agent chat interface for interacting with Large Language Models (LLMs). It features a separation of concerns between a dynamic frontend and a logic-heavy backend, ensuring security, scalability, and ease of integration with organizational APIs.

---

## 🏗️ Architecture Overview

The project is split into two main components:

### 1. Frontend (User Interface)
- **Location**: `/frontend`
- **Technology**: [Streamlit](https://streamlit.io/)
- **Purpose**: Provides a responsive web interface for users to chat with AI agents.
- **Key Features**:
    - **Authentication**: Simple username-based login (expandable to OAuth).
    - **Session Persistence**: Chats are tied to usernames, allowing users to resume conversations.
    - **Real-time Interaction**: Direct communication with the backend API via HTTP.

### 2. Backend (Service Layer)
- **Location**: `/backend`
- **Technology**: [FastAPI](https://fastapi.tiangolo.com/)
- **Purpose**: Acts as the "brain," managing data, external API calls, and agent orchestration.
- **Key Components**:
    - **API Gateway**: Exposes endpoints like `/chat` and `/history`.
    - **Agent Orchestration**: Managed in `agents.py`, coordinating between different specialized AI models.
    - **Database**: Uses SQLite (`sessions.db`) to store chat history locally.
    - **Security**: Handles sensitive credentials (like `GOOGLE_API_KEY`) away from the user's browser.

---

## 🚀 Getting Started

We provide scripts to simplify the setup and execution on both Windows and macOS/Linux.

### Prerequisites
- Python 3.9+ installed.

### Setup
Run the setup script for your operating system to create virtual environments and install dependencies:

- **Windows**: `.\setup_env.ps1`
- **macOS/Linux**: `./setup_env.sh` (You may need to run `chmod +x setup_env.sh` first).

### Running the App
Start both the Backend and Frontend services simultaneously using the run script:

- **Windows**: `.\run_app.ps1`
- **macOS/Linux**: `./run_app.sh` (You may need to run `chmod +x run_app.sh` first).

Once running:
- **Frontend**: [http://localhost:8501](http://localhost:8501)
- **Backend API**: [http://localhost:8000](http://localhost:8000)

---

## 📂 Project Structure

```text
TDM-UI/
├── backend/            # FastAPI source code
│   ├── main.py         # Primary API entry point
│   ├── agents.py       # LLM Agent logic
│   ├── utils.py        # Database and token helpers
│   └── sessions.db     # SQLite Database (Git-ignored)
├── frontend/           # Streamlit source code
│   └── app.py          # UI logic
├── .env                # Secret environment variables (Git-ignored)
├── .gitignore          # File exclusion rules
├── run_app.*           # Execution scripts
└── setup_env.*         # Setup scripts
```

## 🛠️ Tech Stack
- **Dashboard**: Streamlit
- **API Framework**: FastAPI
- **Database**: SQLite
- **AI Integration**: Google Generative AI (AI Studio SDK) / Extensible to Org APIs.
- **Languages**: Python, PowerShell, Bash.
