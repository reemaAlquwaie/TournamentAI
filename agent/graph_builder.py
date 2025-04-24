from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agent.state_schema import State
from tools.tools import book_tickets, get_available_seats
from agent.booking import booking
from agent.general import general
from agent.router import route_request
from config.memory import get_memory

def route_decision(state: State): 
    if state["decision"] == "booking":
        return "booking"
    elif state["decision"] == "general":
        return "general"
    else:
        raise ValueError(f"Unexpected decision: {state['decision']}")
    
def route_booking_decision(state: State):
    """Routes to the appropriate tool node or END based on AI message content."""
    # Make sure we have messages
    ai_message = state["messages"][-1]
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return ai_message.tool_calls[0]["name"]

    return END

def build_graph():

    graph_builder = StateGraph(State)


    graph_builder.add_conditional_edges(
        "route_request",
        route_decision,
    {
        "general": "general",
        "booking": "booking",
    },
)

    graph_builder.add_conditional_edges(
        "booking",
        route_booking_decision,
        ["book_tickets","get_available_seats", END],
    )



    graph_builder.add_node("book_tickets",  ToolNode([book_tickets]))
    graph_builder.add_node("get_available_seats",  ToolNode([get_available_seats]))
    graph_builder.add_node("route_request", route_request)
    graph_builder.add_node("general", general)
    graph_builder.add_node("booking", booking)
    graph_builder.add_edge(START, "route_request")



    graph_builder.add_edge("book_tickets", "booking")
    graph_builder.add_edge("general", END)
    graph_builder.add_edge("get_available_seats", "booking")
    memory = get_memory()
    router_workflow = graph_builder.compile(checkpointer=memory)
    return router_workflow