import time
from functools import lru_cache

from config import get_settings


class AIConfigurationError(RuntimeError):
    pass


@lru_cache
def get_gemini_client():
    from google import genai

    settings = get_settings()

    if not settings.gemini_api_key:
        raise AIConfigurationError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


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

    max_attempts = 4

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            text = (response.text or "").strip()

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text

        except Exception as exc:

            error_text = str(exc)

            retryable = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
                or "temporarily" in error_text.lower()
            )

            # If it is not a temporary error,
            # stop immediately.
            if not retryable:
                raise

            # Last attempt failed
            if attempt == max_attempts - 1:
                raise RuntimeError(
                    "Gemini is temporarily overloaded. "
                    "Please try again in a few seconds."
                ) from exc

            # 1s → 2s → 4s
            delay = 2 ** attempt

            time.sleep(delay)

    raise RuntimeError("Gemini request failed.")