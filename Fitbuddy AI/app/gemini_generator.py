from .config import WORKOUT_MODEL
from .gemini_client import generate_text


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):
    prompt = f"""
You are FitBuddy, a responsible fitness assistant.

Create a simple 7-day workout plan for:

Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:
- Give a safe and simple 7-day plan.
- Include rest or recovery days.
- Keep exercises suitable for general wellness.
- Do not include calorie targets.
- Do not include fasting instructions.
- Do not recommend supplements.
- Avoid extreme exercise.
- Use clear day-by-day formatting.
"""

    try:
        return generate_text(
            WORKOUT_MODEL,
            prompt,
            max_output_tokens=1500
        )

    except Exception:
        return f"""
7-DAY WORKOUT PLAN

Goal: {goal}
Intensity: {intensity}

Day 1:
Light warm-up and simple full-body exercises.
Finish with gentle stretching.

Day 2:
Light walking or another comfortable activity.
Include gentle stretching.

Day 3:
Simple bodyweight exercises such as supported squats,
wall push-ups and easy core exercises.

Day 4:
REST AND RECOVERY DAY

Day 5:
Repeat simple full-body exercises at a comfortable pace.
Include a warm-up and cool-down.

Day 6:
Light walking and gentle mobility exercises.

Day 7:
REST AND RECOVERY DAY

Safety:
Start gradually, take breaks when needed, stay hydrated,
and stop if an exercise causes pain or discomfort.
"""