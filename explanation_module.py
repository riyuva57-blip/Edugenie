 from ai_client import generate_text
from config import get_settings


def explain_concept(text: str) -> str:
    settings = get_settings()

    prompt = (
        "You are an educational assistant.\n\n"
        "Explain the following concept for a beginner.\n"
        "Use simple language.\n"
        "Use short sections.\n"
        "Give one simple example when useful.\n"
        "Avoid unnecessary technical jargon.\n\n"
        f"Concept/request:\n{text}"
    )

    if (
        settings.local_model_enabled
        and settings.explanation_backend.lower() == "local"
    ):
        # Local model is intentionally disabled on Vercel.
        raise RuntimeError(
            "Local explanation model is disabled. "
            "Use Gemini backend."
        )

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=700,
    )