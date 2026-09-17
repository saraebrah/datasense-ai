import json

from llm_client import LLMClient


llm_client = LLMClient()


MAX_QUESTION_LENGTH = 300


def validate_question(question):
    cleaned_question = question.strip()

    if not cleaned_question:
        raise ValueError(
            "Question cannot be empty."
        )

    if len(cleaned_question) > MAX_QUESTION_LENGTH:
        raise ValueError(
            "Question is too long."
        )

    return cleaned_question


def build_qa_prompt(context, question):
    context_json = json.dumps(
        context,
        indent=2,
    )

    return f"""
You are a data analytics assistant.

Answer the user's question using ONLY the
information in the provided analytics context.

Rules:

1. Do not invent numbers or facts.

2. Do not assume information that is not present.

3. If the question cannot be answered from the
provided context, clearly say that there is not
enough information.

4. Do not claim that you queried a database.

5. Keep the answer concise.

6. When useful, mention the exact numbers that
support your answer.

Analytics context:

{context_json}

User question:

{question}
"""


def answer_event_question(
    context,
    question,
):
    cleaned_question = validate_question(
        question
    )

    if context is None:
        raise ValueError(
            "No event data is available."
        )

    prompt = build_qa_prompt(
        context,
        cleaned_question,
    )

    return llm_client.generate_text(
        prompt
    )