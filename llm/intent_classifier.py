from llm.model import gemini_model
from langchain_core.prompts import ChatPromptTemplate
from llm.schemas import Intent

intent_prompt = ChatPromptTemplate.from_template(
    """
You are an AI intent classifier.

Your job is NOT to answer the question.

Your job is to identify:

1. The operation
2. The column

Available Columns:{columns}

User Question:{question}
"""
)

structured_model = gemini_model.with_structured_output(Intent)

def classify_intent(question, columns):
    prompt = intent_prompt.invoke(
        {
            "question": question,
            "columns": ", ".join(columns)
        }
    )

    intent = structured_model.invoke(prompt)

    return intent

