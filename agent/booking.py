from langchain.schema import SystemMessage
from agent.state_schema import State
from config.model import get_llm
from tools.tools import book_tickets, get_available_seats
llm = get_llm()


tools = [book_tickets, get_available_seats]
llm_with_tools = llm.bind_tools(tools)

def booking(state: State):
    
    prompt = f"""
    You are an intelligent assistant that helps users with questions related to the match tickets booking.

    You have access to this tools:
    - get_available_seats tool that can search and return the available seats for the match.
    - buy_tickets to book the selected tickets for the match.

   
    if the user wants to book more than one ticket, you should ask for the number of tickets they want to book.
    if the user want to book a single ticket, you you should call the get_available_seats tool to get the available seats. and ask the user to choose one of the available seats.
    if the user want more than one seats and want them to be closed to each other, you should provide the seats numbers that are closed to each other.
    once the user choose the seats, you should call the book_tickets tool to book the tickets.
    

    Here is the user's message:

    {state["input"]}

    Use the context retrieved from the tool to answer the user's question.
    """

    messages = [
        SystemMessage(content=prompt),
        *state["messages"] 
    ]
    response = llm_with_tools.invoke(messages)

    return {"messages":response,"output": response.content}

   