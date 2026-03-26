from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from config import settings


def connect_sqlite():
    conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
    return SqliteSaver(conn)