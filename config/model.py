from langchain_openai import ChatOpenAI # if you're using HF
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
  
    return ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"

    )

