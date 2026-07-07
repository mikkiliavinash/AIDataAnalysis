from langchain_core.prompts import ChatPromptTemplate


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