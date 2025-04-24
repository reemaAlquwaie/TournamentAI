from typing_extensions import Literal
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from config.model import get_llm
llm = get_llm()
class Route(BaseModel):
    step: Literal["general", "booking"] = Field(
        ..., description="The next step in the routing process"
    )
# Use PydanticOutputParser for structured output
parser = PydanticOutputParser(pydantic_object=Route)
# Routing prompt
router_prompt = PromptTemplate(
    template="""
    Classify the following user query into one of these categories:
    - general → Use this if the user is asking general question like hello, hi or asking about who are you.
    - booking → Use this if the user is asking about the match tickets for booking or any related question.
    Query: {query}
    {format_instructions}
    """,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

def route_request(state):
    """Classify the query and determine which agent should handle it."""
    # Get user query
    query = state["messages"][-1].content
    # Format the prompt
    formatted_prompt = router_prompt.format(query=query)
    llm_response = llm.invoke(formatted_prompt)
    decision = parser.parse(llm_response.content)
    # Ensure LLM returns valid categories
    valid_categories = {"general", "booking"}
 
    if decision.step not in valid_categories:
        raise ValueError(f"Unexpected LLM output: {decision.step}")
    
    return {"decision": decision.step, "input": query}
