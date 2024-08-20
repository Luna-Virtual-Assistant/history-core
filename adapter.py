from interface import HistoryInterface


class HistoryAdapter(HistoryInterface):
    def __init__(self, repository: HistoryInterface):
        self.__repository = repository

    def get_history(self):
        return self.__repository.get_history()

    def add_history(self, command: str, response: str):
        self.__repository.add_history(command, response)