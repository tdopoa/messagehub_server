import os
from contextlib import contextmanager

import pyodbc


class Database:
    def __init__(self) -> None:
        self.server: str = os.environ.get("DB_SERVER")
        self.database: str = os.environ.get("DB_DATABASE")
        self.username: str = os.environ.get("DB_USERNAME")
        self.password: str = os.environ.get("DB_PASSWORD")
        self.connection_string: str = self._build_connection_string()

    def _build_connection_string(self) -> str:
        if self.username and self.password:
            return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        else:
            return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"

    @contextmanager
    def _get_connection(self):
        conn = pyodbc.connect(self.connection_string)
        try:
            yield conn
        finally:
            conn.close()
            conn.close()
