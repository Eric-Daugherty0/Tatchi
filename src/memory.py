import sqlite3
import requests
from pathlib import Path


class TatchiMemory:

    def __init__(self):
        # Store the database in the project's data folder
        project_root = Path(__file__).parent.parent
        data_folder = project_root / "data"

        # Create the data folder if it doesn't exist
        data_folder.mkdir(exist_ok=True)

        self.database = data_folder / "tatchi_memory.db"

        self.create_database()

    # Creates the database to store Tatchi's memories
    def create_database(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        connection.close()

    # Checks whether a memory already exists
    def memory_exists(self, memory):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM memories WHERE memory = ?",
            (memory,)
        )

        result = cursor.fetchone()

        connection.close()

        return result is not None 

        # Checks whether a new memory has the same meaning
    # as a memory already stored in the database.
    def similar_memory(self, memory):

        # Get all existing memories.
        existing_memories = self.get_memories()

        # If there are no memories, there is nothing to compare.
        if not existing_memories:
            return None

        # Create a list of memories for Ollama to compare.
        memory_list = "\n".join(
            f"- {existing_memory}"
            for existing_memory in existing_memories
        )

        prompt = f"""
You are checking whether two memories mean the same thing.

New memory:
{memory}

Existing memories:
{memory_list}

Does the new memory have essentially the same meaning as one
of the existing memories?

If YES, return ONLY the exact existing memory that has the same meaning.

If NO, return ONLY:
NONE
"""

        # Ask the local Ollama AI to compare the memories.
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        answer = result["response"].strip()

        # If Ollama says there is no similar memory,
        # return None.
        if answer.upper() == "NONE":
            return None

        # Return the existing memory that Ollama identified.
        return answer

    # Stores a new memory only if it isn't a duplicate
    # or semantically similar to an existing memory.
    def remember(self, memory):

        # First check for an exact duplicate.
        if self.memory_exists(memory):
            return False

        # Then check for a memory with the same meaning.
        similar = self.similar_memory(memory)

        if similar is not None:
            return False

        # If no duplicate was found, save the new memory.
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO memories (memory) VALUES (?)",
            (memory,)
        )

        connection.commit()
        connection.close()

        return True

    # Retrieves memories from the database
    def get_memories(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT memory FROM memories ORDER BY created_at ASC"
        )

        memories = cursor.fetchall()

        connection.close()

        return [memory[0] for memory in memories]