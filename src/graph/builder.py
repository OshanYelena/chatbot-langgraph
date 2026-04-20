from langgraph.graph import StateGraph, START, END
from src.graph.state import ChatState

# TODO: import node functions once implemented
# from src.graph.nodes.ingest import ingest_user_message
# from src.graph.nodes.context import load_context
# from src.graph.nodes.router import route_intent
# from src.graph.nodes.casual import casual_chat
# from src.graph.nodes.knowledge import knowledge_qa
# from src.graph.nodes.tool import tool_request
# from src.graph.nodes.refusal import safe_refusal
# from src.graph.nodes.postprocess import postprocess_response
# from src.graph.routing.intent import choose_route


def build_graph():
    builder = StateGraph(ChatState)

    # builder.add_node("ingest_user_message", ingest_user_message)
    # builder.add_node("load_context", load_context)
    # builder.add_node("route_intent", route_intent)
    # builder.add_node("casual_chat", casual_chat)
    # builder.add_node("knowledge_qa", knowledge_qa)
    # builder.add_node("tool_request", tool_request)
    # builder.add_node("safe_refusal", safe_refusal)
    # builder.add_node("postprocess_response", postprocess_response)

    # builder.add_edge(START, "ingest_user_message")
    # builder.add_edge("ingest_user_message", "load_context")
    # builder.add_edge("load_context", "route_intent")
    # builder.add_conditional_edges(
    #     "route_intent",
    #     choose_route,
    #     {
    #         "casual": "casual_chat",
    #         "knowledge": "knowledge_qa",
    #         "tool": "tool_request",
    #         "blocked": "safe_refusal",
    #     },
    # )
    # builder.add_edge("casual_chat", "postprocess_response")
    # builder.add_edge("knowledge_qa", "postprocess_response")
    # builder.add_edge("tool_request", "postprocess_response")
    # builder.add_edge("safe_refusal", "postprocess_response")
    # builder.add_edge("postprocess_response", END)

    return builder.compile()
