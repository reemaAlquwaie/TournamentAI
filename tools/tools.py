from langchain_core.tools import tool
from agent.state_schema import State

available_seats = [
    "100",
    "101",
    "300",
    "302",
    "500",
    "600",
    "700",
]
@tool
def get_available_seats(state: State):
    """
    This tool is used to get the available seats for the match.
    Args:
        state (State): A dictionary containing the user's input query in the 'input' key
    Returns:
        dict: A dictionary containing the available seats in the 'available_seats' key
    """


    return {
        "available_seats": available_seats
    }
     
    
@tool
def book_tickets(state: State):
    """
    This tool is used to book the selected tickets for the match.
    Args:
        state (State): A dictionary containing the user's input query in the 'input' key
    Returns:
        dict: A dictionary containing the booked tickets in the 'booked_tickets' key
    """
    
    booked_tickets = state["input"]
   
    return {"booked_tickets": booked_tickets}