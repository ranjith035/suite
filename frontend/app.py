import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ALLOWED_USERS = os.getenv("ALLOWED_USERS", "admin").split(",")

st.set_page_config(page_title="Google ADK Agent", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Authentication & Session State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

# --- Authentication UI ---
def login_screen():
    st.title("🔐 Login")
    st.write("Please enter your organization username to access the Google ADK Agent.")
    
    username = st.text_input("Username").strip().lower()
    
    if st.button("Access Agent"):
        if username in [u.strip().lower() for u in ALLOWED_USERS]:
            st.session_state.authenticated = True
            st.session_state.username = username
            # Tie session_id to username for persistence across devices/logins
            st.session_state.session_id = f"user_{username}" 
            st.success(f"Welcome, {username}!")
            st.rerun()
        elif username == "":
            st.warning("Please enter a username.")
        else:
            st.error("Access Denied: Username not in the approved list.")

# --- Main App Logic ---
if not st.session_state.authenticated:
    login_screen()
else:
    # Use the username-derived session_id
    session_id = st.session_state.session_id

    # Initialize messages if not done
    if "messages" not in st.session_state:
        try:
            response = requests.get(f"{API_URL}/history/{session_id}")
            if response.status_code == 200:
                st.session_state.messages = response.json()
            else:
                st.session_state.messages = []
        except:
            st.session_state.messages = []

    # --- Sidebar ---
    with st.sidebar:
        st.title("Agent Settings")
        st.write(f"Logged in as: **{st.session_state.username}**")
        st.info(f"Identity Key: `{session_id}`")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            if "messages" in st.session_state:
                del st.session_state.messages
            st.rerun()

        if st.button("Clear My History"):
            requests.delete(f"{API_URL}/history/{session_id}")
            st.session_state.messages = []
            st.rerun()

    # --- Main UI ---
    st.title("🤖 Google ADK Agent")
    st.caption(f"Persistent Chat for {st.session_state.username}")

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User Input
    if prompt := st.chat_input("What is on your mind?"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add to local state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Send to backend
        with st.spinner("Agent is thinking..."):
            try:
                payload = {
                    "session_id": session_id,
                    "message": prompt
                }
                response = requests.post(f"{API_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_response = data["response"]
                    
                    with st.chat_message("assistant"):
                        st.write(assistant_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Communication Error: {str(e)}")
