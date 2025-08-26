import uuid

def start_new_conversation():
    thread_id = str(uuid.uuid4())
    checkpoint_ns = "default"   # you can name this anything
    config = {
        "configurable": {
            "thread_id": thread_id,
            "checkpoint_ns": checkpoint_ns
        }
    }
    return config, thread_id

def resume_conversation(saved_thread_id: str):
    """Resume old conversation using saved thread_id"""
    config = {"configurable": {"thread_id": saved_thread_id}}
    return config
