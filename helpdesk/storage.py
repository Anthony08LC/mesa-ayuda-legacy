from pathlib import Path
import sqlite3


def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_schema(connection):
    script = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    connection.executescript(script)


def add_history(connection, ticket_id, event, actor, timestamp):
    connection.execute(
        """
        INSERT INTO ticket_history (ticket_id, event, actor, happened_at)
        VALUES (?, ?, ?, ?)
        """,
        (ticket_id, event, actor, timestamp),
    )
