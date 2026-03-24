from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

def connect_sqlite():
    conn = sqlite3.connect("agent_memory.db", check_same_thread=False)

    checkpointer = SqliteSaver(conn)

    return checkpointer