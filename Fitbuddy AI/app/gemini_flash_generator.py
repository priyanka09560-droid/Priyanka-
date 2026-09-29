from .config import TIP_MODEL
from .gemini_client import generate_text


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
You are FitBuddy, a responsible fitness assistant.

Give one simple nutrition or recovery tip for a person
whose fitness goal is:

{goal}

Requirements:
- Write 2 to 4 simple sentences.
- Focus on balanced meals, hydration, sleep, or recovery.
- Avoid extreme dieting.
- Avoid fasting instructions.
- Avoid calorie targets.
- Avoid supplement prescriptions.
- Use simple and safe language.
"""

    try:
        return generate_text(
            TIP_MODEL,
            prompt,
            max_output_tokens=300
        )

    except Exception:
        return (
            "Focus on balanced meals, regular hydration, "
            "and enough sleep and recovery. "
            "Choose a variety of nutritious foods and "
            "make changes gradually."
        )