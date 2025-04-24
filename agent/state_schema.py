from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
class State(TypedDict):
    input: str
    decision: str
    messages: Annotated[list, add_messages]
    output: str
    available_seats: list
    booked_tickets: list