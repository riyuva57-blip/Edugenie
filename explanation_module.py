from ai_client import generate_text


def explain_concept(text: str) -> str:
    prompt = (
        "Explain the following educational concept for a beginner. "
        "Use plain language, short sections, one simple example when useful, "
        "and avoid unnecessary jargon.\n\n"
        "Concept/request:\n"
        + text
    )

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=700,
    )