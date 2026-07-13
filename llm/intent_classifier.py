from llm.model import llm
from llm.schemas import Intent
from llm.prompts.intent_prompt import intent_prompt

structured_model = llm.with_structured_output(Intent)

def classify_intent(question, columns):
    prompt = intent_prompt.invoke(
        {
            "question": question,
            "columns": ", ".join(columns),
        }
    )

    intent = structured_model.invoke(prompt)
    print("=======================")
    print(intent)

    return intent