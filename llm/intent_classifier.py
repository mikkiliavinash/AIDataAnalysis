from llm.model import llm
from llm.schemas import Intent
from llm.prompts.intent_prompt import intent_prompt

structured_model = llm.with_structured_output(Intent)

def classify_intent(question, metadata):
    prompt = intent_prompt.invoke(
        {
            "question": question,
            "metadata": metadata
        }
    )
    intent = structured_model.invoke(prompt)
    return intent