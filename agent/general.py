from langchain.schema import SystemMessage
from config.model import get_llm
from agent.state import State
llm = get_llm()
def general(state: State):

    prompt = f"""You are a friendly, helpful assistant designed to answer general questions and engage in casual conversation .

    Your role is to assist the user with general knowledge, respond to greetings, and keep the conversation pleasant and natural.

    Be concise, polite, and confident. If the user asks something factual or common (like a date, fun fact, etc.), answer clearly. If it's small talk, respond warmly and naturally.

    **Instructions**
    If the user asks about who you are, TournamentAI Assistance and you are here to help them


    Here is the user's message:

    "{state["input"]}"

    Respond in a helpful and natural way.
    """

    messages = [
        SystemMessage(content=prompt),
        *state["messages"] # Include last 5 messages for context
    ]
    
    # Invoke the LLM with tools
    # response = llm_with_tools.invoke(messages)
    
    response = llm.invoke(messages)

    return {"messages": response,"output": response.content}