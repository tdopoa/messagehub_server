import os
from contextlib import contextmanager
from typing import Optional

import pyodbc


class Database:
    def __init__(self) -> None:
        self.server: str = self._get_required_env("DB_SERVER")
        self.database: str = self._get_required_env("DB_DATABASE")
        self.username: Optional[str] = os.environ.get("DB_USERNAME")
        self.password: Optional[str] = os.environ.get("DB_PASSWORD")
        self.connection_string: str = self._build_connection_string()

    def _get_required_env(self, key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

    def _build_connection_string(self) -> str:
        if self.username and self.password:
            return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"

    @contextmanager
    def _get_connection(self):
        conn = None
        try:
            conn = pyodbc.connect(self.connection_string)
            yield conn
        finally:
            if conn:
                conn.close()
