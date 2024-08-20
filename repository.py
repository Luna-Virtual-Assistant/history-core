import psycopg2
from interface import HistoryInterface

class PostgresHistoryRepository(HistoryInterface):
    def __init__(self, connection_string: str):
        self.connection = psycopg2.connect(connection_string)
        self.__migrate()
    
    def get_history(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM history")
            result = cursor.fetchall()
            return [row[0] for row in result]
    
    def add_history(self, command: str, response: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO history (command, response) VALUES (%s, %s)", (command, response))
        self.connection.commit()

    def __migrate(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history (
                        id SERIAL PRIMARY KEY,
                        command VARCHAR(255) NOT NULL,
                        response TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                self.connection.commit()
        except Exception as error:
            print(f"Error creating table: {error}")
            self.connection.rollback()