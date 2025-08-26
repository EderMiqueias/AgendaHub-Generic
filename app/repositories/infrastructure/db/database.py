class Database:
    def get_connection(self):
        raise NotImplementedError

    def fetch_all(self, query: str, params: tuple = ()):
        raise NotImplementedError

    def fetch_one(self, query: str, params: tuple = ()):
        raise NotImplementedError

    def execute_query(self, query: str, params: tuple = ()):
        raise NotImplementedError


__all__ = ['Database']
