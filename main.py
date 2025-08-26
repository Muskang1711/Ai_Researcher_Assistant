# from fastapi import FastAPI
# from pydantic import BaseModel

# from ai_researcher_langgraph import graph, INITIAL_PROMPT
# from db import checkpointer, conn
# from utils import start_new_conversation, resume_conversation


# # Compile graph with persistence
# compiled_graph = graph.compile(checkpointer=checkpointer)

# app = FastAPI(title="AI Researcher")

# # --- Pydantic Model ---
# class UserMessage(BaseModel):
#     content: str

# # --- Endpoints ---
# @app.post("/new_chat")
# def new_chat():
#     """Start a new conversation"""
#     config, thread_id = start_new_conversation()
#     # inject INITIAL_PROMPT only once, at chat creation
#     input_data = {
#         "messages": [
#             {"role": "system", "content": INITIAL_PROMPT}
#         ]
#     }
#     compiled_graph.invoke(input_data, config)
#     return {"thread_id": thread_id}

# @app.post("/send_message/{thread_id}")
# def send_message(thread_id: str, msg: UserMessage):
#     """Send user message to graph"""
#     config = resume_conversation(thread_id)
#     input_data = {
#         "messages": [
#             {"role": "user", "content": msg.content}
#         ]
#     }
#     result = compiled_graph.invoke(input_data, config)

#     # Safely extract last reply
#     reply_msg = result["messages"][-1]
#     reply = getattr(reply_msg, "content", str(reply_msg))

#     return {"reply": reply}

# @app.get("/chats")
# def list_chats():
#     """List all saved thread_ids"""
#     with conn:  # ensures cursor cleanup
#         cursor = conn.cursor()
#         cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
#         chats = [row[0] for row in cursor.fetchall()]
#     return {"chats": chats}


# @app.get("/history/{thread_id}")
# def get_history(thread_id: str):
#     """Get full conversation history"""
#     with conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT value 
#             FROM checkpoints 
#             WHERE thread_id = ?
#             ORDER BY id ASC
#         """, (thread_id,))
#         rows = cursor.fetchall()

#     # Each row["value"] is stored JSON, so decode messages
#     import json
#     history = []
#     for row in rows:
#         try:
#             checkpoint = json.loads(row[0])
#             msgs = checkpoint.get("messages", [])
#             history.extend(msgs)
#         except Exception:
#             continue
#     return {"history": history}


# from fastapi import FastAPI
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel

# from ai_researcher_langgraph import graph, INITIAL_PROMPT
# from db import checkpointer, conn
# from utils import start_new_conversation, resume_conversation

# # Compile graph with persistence
# compiled_graph = graph.compile(checkpointer=checkpointer)

# app = FastAPI(title="AI Researcher")

# # --- Mount static directory (for frontend.html, css, js etc.) ---
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # --- Serve Frontend ---
# @app.get("/")
# def serve_frontend():
#     return FileResponse("frontend.html")


# # --- Pydantic Model ---
# class UserMessage(BaseModel):
#     content: str


# # --- API Endpoints ---
# @app.post("/new_chat")
# def new_chat():
#     """Start a new conversation"""
#     config, thread_id = start_new_conversation()
#     input_data = {
#         "messages": [
#             {"role": "system", "content": INITIAL_PROMPT}
#         ]
#     }
#     checkpointer.put(config, {"messages": input_data["messages"]})
#     return {"thread_id": thread_id}


# @app.post("/send_message/{thread_id}")
# def send_message(thread_id: str, msg: UserMessage):
#     """Send user message to graph"""
#     config = resume_conversation(thread_id)
#     input_data = {
#         "messages": [
#             {"role": "user", "content": msg.content}
#         ]
#     }
#     result = compiled_graph.invoke(input_data, config)

#     reply_msg = result["messages"][-1]
#     reply = getattr(reply_msg, "content", str(reply_msg))

#     return {"reply": reply}


# @app.get("/chats")
# def list_chats():
#     """List all saved thread_ids"""
#     with conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
#         chats = [row[0] for row in cursor.fetchall()]
#     return {"chats": chats}


# @app.get("/history/{thread_id}")
# def get_history(thread_id: str):
#     """Get full conversation history"""
#     with conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT value 
#             FROM checkpoints 
#             WHERE thread_id = ?
#             ORDER BY id ASC
#         """, (thread_id,))
#         rows = cursor.fetchall()

#     import json
#     history = []
#     for row in rows:
#         try:
#             checkpoint = json.loads(row[0])
#             msgs = checkpoint.get("messages", [])
#             history.extend(msgs)
#         except Exception:
#             continue
#     return {"history": history}


from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ai_researcher_langgraph import graph, INITIAL_PROMPT
from db import checkpointer, conn
from utils import start_new_conversation, resume_conversation

import uuid

# Compile graph with persistence
compiled_graph = graph.compile(checkpointer=checkpointer)

app = FastAPI(title="AI Researcher")

# --- Mount static directory (for frontend.html, css, js etc.) ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Serve Frontend ---
@app.get("/")
def serve_frontend():
    return FileResponse("frontend.html")


# --- Pydantic Model ---
class UserMessage(BaseModel):
    content: str


# --- API Endpoints ---
@app.post("/send_message")
def send_message(msg: UserMessage):
    """Send user message to graph. Thread handled internally."""

    # Always create a new thread if none exists
    config, thread_id = start_new_conversation()

    # Insert system prompt if first message
    input_data = {
        "messages": [
            {"role": "system", "content": INITIAL_PROMPT},
            {"role": "user", "content": msg.content}
        ]
    }

    # # Store system + user message in DB
    # checkpointer.put(
    #     config,
    #     {"messages": input_data["messages"]},
    #     metadata={},
    #     new_versions={"messages": len(input_data["messages"])}
    # )

    # Run graph
    result = compiled_graph.invoke(input_data, config)

    # Get last reply
    reply_msg = result["messages"][-1]
    reply = getattr(reply_msg, "content", str(reply_msg))

    return {"reply": reply}


@app.get("/chats")
def list_chats():
    """List all saved thread_ids (for debugging / admin use)"""
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        chats = [row[0] for row in cursor.fetchall()]
    return {"chats": chats}


@app.get("/history/{thread_id}")
def get_history(thread_id: str):
    """Get full conversation history by thread_id"""
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value 
            FROM checkpoints 
            WHERE thread_id = ?
            ORDER BY id ASC
        """, (thread_id,))
        rows = cursor.fetchall()

    import json
    history = []
    for row in rows:
        try:
            checkpoint = json.loads(row[0])
            msgs = checkpoint.get("messages", [])
            history.extend(msgs)
        except Exception:
            continue
    return {"history": history}


