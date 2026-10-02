import json
import re
from typing import Any

from ai_client import generate_text


def clean_json_block(text: str) -> str:
    """Remove common Markdown fences and isolate the outer JSON object/array."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start_candidates = [p for p in (cleaned.find("["), cleaned.find("{")) if p >= 0]
    if start_candidates:
        start = min(start_candidates)
        end = max(cleaned.rfind("]"), cleaned.rfind("}"))
        if end >= start:
            cleaned = cleaned[start : end + 1]
    return cleaned.strip()


def _extract_questions(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("questions", "quiz", "items"):
            if isinstance(payload.get(key), list):
                return payload[key]
        raise ValueError("JSON object does not contain a questions list.")
    if isinstance(payload, list):
        return payload
    raise ValueError("Quiz JSON must be a list or an object containing a questions list.")


def _normalize_question(item: dict[str, Any]) -> dict[str, Any]:
    options = item.get("options") or item.get("choices")
    answer = item.get("correct_answer") or item.get("correctAnswer") or item.get("answer")
    question = item.get("question") or item.get("prompt")
    if not isinstance(question, str) or not isinstance(options, list) or not isinstance(answer, str):
        raise ValueError("Each quiz item needs question, options, and correct_answer fields.")
    options = [str(option).strip() for option in options]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError("Each quiz question must contain exactly four unique options.")
    answer = answer.strip()
    if answer not in options:
        # Accept an answer index such as 0/1/2/3 or A/B/C/D.
        match = re.fullmatch(r"(?:option\s*)?([A-D]|[0-3])", answer, re.I)
        if match:
            raw = match.group(1).upper()
            idx = ord(raw) - ord("A") if raw in "ABCD" else int(raw)
            answer = options[idx]
        else:
            raise ValueError("correct_answer must match one of the four options.")
    return {
        "question": question.strip(),
        "options": options,
        "correct_answer": answer,
        "explanation": str(item.get("explanation", "")).strip(),
    }


def generate_quiz(text: str) -> list[dict[str, Any]]:
    prompt = f"""Create exactly three multiple-choice questions from the educational text below.
Each question must have exactly four plausible options and exactly one correct answer.
Return ONLY valid JSON in this shape:
{{"questions":[{{"question":"...","options":["...","...","...","..."],"correct_answer":"...","explanation":"..."}}]}}
The correct_answer value must exactly equal one of the option strings.
Do not use Markdown fences.

SOURCE TEXT:
{text}
"""
    raw = generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=1800,
        response_mime_type="application/json",
    )
    payload = json.loads(clean_json_block(raw))
    questions = [_normalize_question(item) for item in _extract_questions(payload)]
    if len(questions) != 3:
        raise ValueError(f"Expected exactly 3 questions, received {len(questions)}.")
    return questions
