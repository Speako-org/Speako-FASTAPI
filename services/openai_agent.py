from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


def chat_with_openai(message: str) -> str:
    response = llm([HumanMessage(content=message)])
    return response.content