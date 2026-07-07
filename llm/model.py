from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

gemini_model=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    max_tokens=500
)
