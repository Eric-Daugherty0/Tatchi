import sqlite3 
from pathlib import Path 

class TatchiMemory: 
    def __init__(self):
        # Store the database in the project's data folder
        project_root = Path(__file__).parent.parent
        data_folder = project_root / "data"

        # Create the data folder if it doesn't exsist
        data_folder.mkdir(exist_ok=True)

        self.database = data_folder / "tatchi_memory.db"

        self.create_database()
        # Creates the Database to store the memory of the AI
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

    def remeber(self, memory):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        # Actually using insert to create a row in the database to store the information I asked it to. 
        cursor.execute(
            "INSERT INTO memories (memory) VALUES (?)",
            (memory,)
        )

        connection.commit()
        connection.close()
        
    def get_memories(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor() 
        # Retrieves the memory 
        cursor.execute(
            "SELECT memory FROM memories ORDER BY created_at ASC"
        )

        memories = cursor.fetchall()

        connection.close()

        return [memory[0] for memory in memories]