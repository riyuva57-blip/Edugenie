from functools import lru_cache

from config import get_settings
from ai_client import generate_text


@lru_cache(maxsize=1)
def _load_local_pipeline():
    """Load LaMini lazily so the FastAPI process can start without downloading a model."""
    from transformers import pipeline

    settings = get_settings()
    return pipeline(
        "text2text-generation",
        model=settings.explanation_model,
        device=-1,
    )


def explain_concept(text: str) -> str:
    settings = get_settings()
    prompt = (
        "Explain the following educational concept for a beginner. "
        "Use plain language, short sections, one simple example when useful, "
        "and avoid unnecessary jargon.\n\nConcept/request:\n" + text
    )

    if settings.local_model_enabled and settings.explanation_backend.lower() == "local":
        generator = _load_local_pipeline()
        result = generator(prompt, max_new_tokens=300, do_sample=False)[0]["generated_text"]
        return result.strip()

    return generate_text(prompt, temperature=0.2, max_output_tokens=700)
