from functools import lru_cache

from config import get_settings


class AIConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_gemini_client():
    from google import genai

    settings = get_settings()

    if not settings.gemini_api_key:
        raise AIConfigurationError(
            "GEMINI_API_KEY is not configured in Vercel Environment Variables."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.3,
    max_output_tokens: int = 2048,
    response_mime_type: str | None = None,
) -> str:

    settings = get_settings()
    client = get_gemini_client()

    from google.genai import types

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        response_mime_type=response_mime_type,
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )

    text = (response.text or "").strip()

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text