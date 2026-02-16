import google.generativeai as genai
import os
import logging
import json

logger = logging.getLogger("TDM-API.Agents")

# --- Load Prompts ---
def load_prompts():
    prompts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.json")
    try:
        with open(prompts_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load prompts.json, using minimal defaults: {e}")
        return {
            "orchestrator": "You are the Orchestrator agent.",
            "researcher": "You are a Researcher agent.",
            "analyst": "You are an Analyst agent."
        }

AGENT_PROMPTS = load_prompts()

class Agent:
    def __init__(self, name: str, instruction: str, model_name: str = "gemini-1.5-flash"):
        self.name = name
        self.instruction = instruction
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Initializing Agent: {self.name} with model {self.model_name}")
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

class MultiAgentSystem:
    def __init__(self):
        # We'll initialize these lazily
        self._orchestrator = None
        self._researcher = None
        self._analyst = None

    def _ensure_agents(self):
        if self._orchestrator is None:
            self._orchestrator = Agent("Orchestrator", AGENT_PROMPTS.get("orchestrator", ""), "gemini-flash-latest")
            self._researcher = Agent("Researcher", AGENT_PROMPTS.get("researcher", ""), "gemini-flash-latest")
            self._analyst = Agent("Analyst", AGENT_PROMPTS.get("analyst", ""), "gemini-flash-latest")

    async def run(self, user_input: str, history=None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
             logger.error("API Key missing during agent execution.")
             return "SYSTEM ERROR: Google AI Studio API Key (GOOGLE_API_KEY) is not configured in .env."

        try:
            self._ensure_agents()
            
            # 1. Start with Orchestrator
            logger.info("Calling Orchestrator Agent...")
            orch_chat = self._orchestrator.get_chat(history=history or [])
            response = orch_chat.send_message(user_input)
            response_text = response.text

            # 2. Simple Routing Logic (Prototype Handoff)
            if "RESEARCHER:" in response_text:
                query = response_text.split("RESEARCHER:")[1].strip()
                logger.info(f"Orchestrator handing off to RESEARCHER: {query}")
                res_chat = self._researcher.get_chat()
                res_response = res_chat.send_message(query)
                # Synthesis call
                logger.info("Researcher returned data. Synthesizing final answer...")
                response = orch_chat.send_message(f"RESEARCHER returned: {res_response.text}. Now synthesize the final answer for the user.")
                return response.text
            
            elif "ANALYST:" in response_text:
                query = response_text.split("ANALYST:")[1].strip()
                logger.info(f"Orchestrator handing off to ANALYST: {query}")
                ana_chat = self._analyst.get_chat()
                ana_response = ana_chat.send_message(query)
                # Synthesis call
                logger.info("Analyst returned data. Synthesizing final answer...")
                response = orch_chat.send_message(f"ANALYST returned: {ana_response.text}. Now synthesize the final answer for the user.")
                return response.text
            
            return response_text
        except Exception as e:
            logger.exception("Exception occurred in MultiAgentSystem.run")
            return f"AGENT ERROR: {str(e)}"
