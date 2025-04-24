from typing_extensions import Literal, TypedDict
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.schema import AIMessage
import requests
class State(TypedDict):
    input: str
    decision: str
    messages: Annotated[list, add_messages]
    output: str
    available_seats: list
    booked_tickets: list