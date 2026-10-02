from ai_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner", weeks: int = 6) -> str:
    prompt = f"""Create a structured learning path for the topic: {topic}
Learner level: {level}
Time horizon: {weeks} weeks

Requirements:
- Start at the requested level and progress toward more advanced material.
- Organize the plan week by week.
- Give concepts/topics, practical activities, and a simple checkpoint for each week.
- Suggest resource TYPES (documentation, textbook, video course, practice site, etc.).
- Do not invent exact URLs or claim a resource was checked.
- Keep the plan realistic for a self-learner.
"""
    return generate_text(prompt, temperature=0.4, max_output_tokens=1800)
