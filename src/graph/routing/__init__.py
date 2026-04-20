from src.graph.state import ChatState


def choose_route(state: ChatState) -> str:
    """Read intent from state and return the next node name."""
    return state["intent"]
