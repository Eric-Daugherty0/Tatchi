import requests 
from memory import TatchiMemory

# The class is the blueprint for the actual robot. 
class TatchiAssistant:
    # Runs one time and is initializing everything.
    def __init__(self):
        # This is used to tell exactly where ollama is.
        self.ollama_url = "http://localhost:11434/api/generate"
        # Tells AI what model to use.
        self.model = "qwen2.5:1.5b"

        self.memory = TatchiMemory()
        # System prompt that is sent to the AI to understand the task. 
        self.system_prompt = """
You are Tatchi, a personal AI assistant running locally
on a Raspberry pi 5.

Your name is Tatchi. Never introduce yourself as Qwen.
Qwen is the language model you use, but your identity is Tatchi. 

You are helpful, intelligent, friendly, and straightfoward.

You assist your user with questions, projects, programming,
technology, and everyday tasks.

You have access to memories about your user.
Use these memories when they are relevant to the user's question.
Do not claim you forgot something if the information is present
in your memories.
"""
    # Ask function takes your question and stores it inside message
    def ask(self, message):
        memories = self.memory.get_memories()

        memory_text = ""

        if memories:
            memory_text = """ 
IMPORTANT: the following information has been saved in Tatchi's
long-term memory. Use this information when it is relevant.

"""

            for memory in memories:
                memory_text += f"MEMORY: {memory}\n"

        prompt = f""" 
{self.system_prompt}

{memory_text}

USER QUESTION:
{message}

TATCHI RESPONSE:
"""

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        } 
        # This is kind of like an http request. Python takes the information to ollama so it can be answered. 
        response = requests.post(
            self.ollama_url,
            json=data,
            timeout=120
        )

        response.raise_for_status()
        # Python converts the json into a python dictionary and extracts my information from Results["response"]
        result = response.json()

        return result["response"]

    def remember(self, information):
        self.memory.remeber(information)