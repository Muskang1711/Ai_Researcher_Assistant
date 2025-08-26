import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# SQLite connection
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
conn.row_factory = sqlite3.Row


# LangGraph checkpointer
checkpointer = SqliteSaver(conn)
