from llm.model import gemini_model
from llm.schemas import Intent
from llm.prompts.intent_prompt import intent_prompt

structured_model = gemini_model.with_structured_output(Intent)

def classify_intent(question, columns):
    prompt = intent_prompt.invoke(
        {
            "question": question,
            "columns": ", ".join(columns),
        }
    )

    intent = structured_model.invoke(prompt)

    return intent