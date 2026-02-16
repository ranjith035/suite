import google.generativeai as genai
import os

class Agent:
    def __init__(self, name: str, instruction: str, model_name: str = "gemini-1.5-flash"):
        self.name = name
        self.instruction = instruction
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            # Configure API Key if not already configured
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and not genai.get_model("models/" + self.model_name): # Simple check or just apply
                 genai.configure(api_key=api_key)
            
            self._model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.instruction
            )
        return self._model

    def get_chat(self, history=None):
        return self.model.start_chat(history=history)

# --- Define Specialized Agents ---

RESEARCHER_INSTR = """You are a Researcher Agent. 
Your goal is to gather detailed factual information and provide concise summaries. 
When asked a question, focus on the 'what', 'where', and 'when'."""

ANALYST_INSTR = """You are an Analyst Agent. 
Your goal is to process information provided to you and provide deep insights, pros/cons, or logical deductions.
Focus on the 'why' and 'how'."""

ORCHESTRATOR_INSTR = """You are the Orchestrator (Manager) Agent.
You have two sub-agents:
1. Researcher: For finding facts.
2. Analyst: For processing and reasoning.

When a user asks a question:
1. If it's simple, answer it directly.
2. If it requires data, say: 'RESEARCHER: [Query for facts]'
3. If it requires reasoning, say: 'ANALYST: [Context for analysis]'

You are the only agent the user sees. You must synthesize the final answer."""

class MultiAgentSystem:
    def __init__(self):
        # We'll initialize these lazily
        self._orchestrator = None
        self._researcher = None
        self._analyst = None

    def _ensure_agents(self):
        if self._orchestrator is None:
            self._orchestrator = Agent("Orchestrator", ORCHESTRATOR_INSTR, "gemini-flash-latest")
            self._researcher = Agent("Researcher", RESEARCHER_INSTR, "gemini-flash-latest")
            self._analyst = Agent("Analyst", ANALYST_INSTR, "gemini-flash-latest")

    async def run(self, user_input: str, history=None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
             return "SYSTEM ERROR: Google AI Studio API Key (GOOGLE_API_KEY) is not configured in .env."

        try:
            self._ensure_agents()
            
            # 1. Start with Orchestrator
            orch_chat = self._orchestrator.get_chat(history=history or [])
            response = orch_chat.send_message(user_input)
            response_text = response.text

            # 2. Simple Routing Logic (Prototype Handoff)
            if "RESEARCHER:" in response_text:
                query = response_text.split("RESEARCHER:")[1].strip()
                res_chat = self._researcher.get_chat()
                res_response = res_chat.send_message(query)
                # Synthesis call
                response = orch_chat.send_message(f"RESEARCHER returned: {res_response.text}. Now synthesize the final answer for the user.")
                return response.text
            
            elif "ANALYST:" in response_text:
                query = response_text.split("ANALYST:")[1].strip()
                ana_chat = self._analyst.get_chat()
                ana_response = ana_chat.send_message(query)
                # Synthesis call
                response = orch_chat.send_message(f"ANALYST returned: {ana_response.text}. Now synthesize the final answer for the user.")
                return response.text
            
            return response_text
        except Exception as e:
            return f"AGENT ERROR: {str(e)}"
