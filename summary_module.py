from ai_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""Summarize the educational passage below for quick revision.
Keep the central facts, definitions, relationships, and conclusions.
Remove repetition and minor detail. Use a short heading and bullet points when helpful.
Do not introduce facts that are not supported by the passage.

PASSAGE:
{text}
"""
    return generate_text(prompt, temperature=0.2, max_output_tokens=1200)
