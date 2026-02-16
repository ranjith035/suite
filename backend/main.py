import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from utils import SessionManager, TokenManager, Message
from agents import MultiAgentSystem
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Google ADK Multi-Agent API")
session_manager = SessionManager(db_path="sessions.db")
token_manager = TokenManager(auth_api_url=os.getenv("AUTH_API_URL"))

# Configure AI Studio
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: GOOGLE_API_KEY not found in environment.")

# Initialize Multi-Agent System
multi_agent = MultiAgentSystem()

@app.get("/")
async def root():
    return {"status": "ok", "service": "Google ADK Multi-Agent API", "sdk": "AI Studio"}

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    history: List[Message]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 1. Get History from SQLite
        history = session_manager.get_history(request.session_id)
        
        # 2. Convert to AI Studio format
        # History format: [{'role': 'user', 'parts': ['...']}, {'role': 'model', 'parts': ['...']}]
        sdk_history = []
        for msg in history:
            role = "user" if msg.role == "user" else "model"
            sdk_history.append({"role": role, "parts": [msg.content]})
            
        # 3. Run Multi-Agent Orchestration
        response_text = await multi_agent.run(request.message, history=sdk_history)
        
        # 4. Save to SQLite
        session_manager.save_message(request.session_id, "user", request.message)
        session_manager.save_message(request.session_id, "assistant", response_text)
        
        # 5. Return updated history
        updated_history = session_manager.get_history(request.session_id)
        
        return ChatResponse(response=response_text, history=updated_history)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}", response_model=List[Message])
async def get_history(session_id: str):
    return session_manager.get_history(session_id)

@app.delete("/history/{session_id}")
async def clear_history(session_id: str):
    session_manager.clear_history(session_id)
    return {"status": "cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
