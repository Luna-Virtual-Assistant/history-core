from adapter import HistoryAdapter
from repository import PostgresHistoryRepository

class HistoryFactory:
    def get_history(self, use_db: bool = False, connection_string: str = None):
        if use_db and connection_string:
            repository = PostgresHistoryRepository(connection_string)
        return HistoryAdapter(repository)
