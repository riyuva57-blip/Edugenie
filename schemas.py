from typing import Literal
from pydantic import BaseModel, Field, field_validator

MAX_INPUT_CHARS = 30_000


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)

    @field_validator("text")
    @classmethod
    def non_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be blank.")
        return value


class LearningPathRequest(TextRequest):
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    weeks: int = Field(default=6, ge=1, le=52)


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str = Field(min_length=1)
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str = Field(min_length=1)
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)
