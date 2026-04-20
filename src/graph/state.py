from typing import TypedDict


class ChatState(TypedDict):
    messages: list          # Full conversation history
    user_id: str            # Identifies the user
    thread_id: str          # Identifies the conversation thread
    intent: str             # Routing outcome: casual | knowledge | tool | blocked
    retrieved_docs: list    # Documents surfaced by the RAG pipeline
    tool_results: list      # Results returned by tool execution
    response: str           # Final response string to be streamed
