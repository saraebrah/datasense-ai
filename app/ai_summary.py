import json

from llm_client import LLMClient

llm_client = LLMClient()

def build_summary_prompt(context):
    context_json = json.dumps(
        context,
        indent=2,
    )

    return f"""
You are analyzing product usage data.

Use ONLY the facts provided below.

Do not invent values or facts that are not present.

Write a concise summary for a product or data analyst.

Include:
- overall activity
- the most common event types
- notable user activity
- any obvious patterns
- 2 to 4 short analytical observations

Data:

{context_json}
"""


def generate_event_summary(context):
    prompt = build_summary_prompt(context)

    return llm_client.generate_text(prompt)