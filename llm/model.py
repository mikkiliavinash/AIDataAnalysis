from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)
