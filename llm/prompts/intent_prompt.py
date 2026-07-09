from langchain_core.prompts import ChatPromptTemplate

intent_prompt = ChatPromptTemplate.from_template("""
You are an AI intent classifier.

Your job is NOT to answer the question.

Extract the following information:

1. operation
2. column
3. filter_column
4. filter_value

Rules:

- operation should be one of:
  MAX, MIN, SUM, AVERAGE

- column must be one of the available columns.

- If the user applies a filter, extract:
    filter_column
    filter_value

- If there is no filter, return null for
  filter_column and filter_value.

Available Columns:
{columns}

User Question:
{question}
                                                                          
""")