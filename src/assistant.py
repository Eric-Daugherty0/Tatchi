import requests
from memory import TatchiMemory


# The class is the blueprint for Tatchi's AI assistant.
class TatchiAssistant:

    # Runs when Tatchi starts and initializes everything.
    def __init__(self):

        # Tells Python where Ollama is running.
        self.ollama_url = "http://localhost:11434/api/generate"

        # Tells Ollama which AI model Tatchi uses.
        self.model = "qwen2.5:1.5b"

        # Connect Tatchi to its long-term memory system.
        self.memory = TatchiMemory()

        # Instructions that define Tatchi's identity and behavior.
        self.system_prompt = """
You are Tatchi, a personal AI assistant running locally
on a Raspberry Pi 5.

Your name is Tatchi. Never introduce yourself as Qwen.
Qwen is the language model you use, but your identity is Tatchi.

You are helpful, intelligent, friendly, and straightforward.

You assist your user with questions, projects, programming,
technology, and everyday tasks.

You have access to memories about your user.
Use these memories when they are relevant to the user's question.

Do not claim you forgot something if the information is present
in your memories.
"""

    # Sends the user's message to Tatchi.
    def ask(self, message):

        # Get Tatchi's saved memories.
        memories = self.memory.get_memories()

        memory_text = ""

        # If Tatchi has memories, add them to the prompt.
        if memories:
            memory_text = """
IMPORTANT: The following information has been saved
in Tatchi's long-term memory.

Use this information when it is relevant.

"""

            for memory in memories:
                memory_text += f"MEMORY: {memory}\n"

        # Build the prompt sent to Ollama.
        prompt = f"""
{self.system_prompt}

{memory_text}

USER QUESTION:
{message}

TATCHI RESPONSE:
"""

        # Information sent to Ollama.
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        # Send the request to Ollama.
        response = requests.post(
            self.ollama_url,
            json=data,
            timeout=120
        )

        # Stop if Ollama reports an error.
        response.raise_for_status()

        # Convert Ollama's JSON response into Python data.
        result = response.json()

        # Return Tatchi's response.
        return result["response"]

    # Determines whether something should be remembered.
    def should_remember(self, message):

        prompt = f"""
You are Tatchi's memory filter.

Your ONLY job is to decide if the user's statement
contains information that should be saved for future conversations.

SAVE information such as:

- The user's name
- Favorite things
- Likes and dislikes
- Personal preferences
- Important goals
- Important projects
- Long-term plans
- Important instructions

DO NOT SAVE:

- Questions
- Greetings
- Jokes
- General facts
- Temporary information
- Random conversation

Return ONLY:

YES

or

NO

USER STATEMENT:
{message}

ANSWER:
"""

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.ollama_url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        decision = result["response"].strip().upper()

        # Show us what Tatchi decided while we are testing.
        print(f"[Memory Check: {decision}]")

        return decision.startswith("YES")

    # Extracts the important information from the user's message.
    def extract_memory(self, message):

        prompt = f"""
You are Tatchi's memory extraction system.

The user said:

"{message}"

Extract the important information that should be remembered
for future conversations.

Rewrite it as a short, clear statement.

Do not add information that the user did not provide.

Examples:

User:
"My favorite animal is a cheetah."

Memory:
"User's favorite animal is a cheetah."

User:
"I'm building a robot assistant called Tatchi."

Memory:
"User is building a robot assistant called Tatchi."

User:
"I prefer Python over Java."

Memory:
"User prefers Python over Java."

Return ONLY the memory statement.
"""

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.ollama_url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["response"].strip()

    # Saves information into Tatchi's long-term memory.
    def remember(self, information):

        return self.memory.remember(information)

