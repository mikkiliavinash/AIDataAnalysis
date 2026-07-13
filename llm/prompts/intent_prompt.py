from langchain_core.prompts import ChatPromptTemplate

intent_prompt = ChatPromptTemplate.from_template("""You are an intent classifier.

Extract:

1. operation
2. column
3. filters
4. group_by
5. sort_by
6. sort_order
7. top_n
8. bottom_n

Rules:

Aggregation operations:

SUM
AVERAGE
MAX
MIN
COUNT

Only return an operation if the user asks for an aggregation.

Examples:

"What is the total amount?"
operation = SUM

"Average amount by FLAG"
operation = AVERAGE

"Count by FLAG"
operation = COUNT

----------------------------------

Sorting:

If the user asks to sort data,
leave operation as null.

Extract:

sort_by
sort_order

Example:

Sort HOA by AMOUNT ascending

operation = null
column = HOA
sort_by = AMOUNT
sort_order = ASC

----------------------------------

Top N

Top 10 HOA by Amount

operation = null
column = HOA
sort_by = AMOUNT
sort_order = DESC
top_n = 10

----------------------------------

Bottom N

Lowest 5 HOA by Amount

operation = null
column = HOA
sort_by = AMOUNT
sort_order = ASC
bottom_n = 5

----------------------------------

Filters

Extract every filter.

----------------------------------

Available columns:

{columns}

Question:

{question}
                                                                          
""")