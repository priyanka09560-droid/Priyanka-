from .gemini_client import generate_text


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):
    prompt = f"""
You are FitBuddy, a responsible fitness assistant.

Original workout plan:
{original_plan}

User goal:
{goal}

Workout intensity:
{intensity}

User feedback:
{feedback}

Create an updated version of the workout plan based on the feedback.

Keep it simple, safe and suitable for general wellness.
Do not include extreme exercise, calorie targets, fasting instructions,
or supplement prescriptions.

Return the updated workout plan clearly.
"""

    try:
        return generate_text(
            "gemini-3.6-flash",
            prompt,
            max_output_tokens=1500
        )

    except Exception:
        return (
            original_plan
            + "\n\n"
            + "Updated based on your feedback:\n"
            + feedback
            + "\n\n"
            + "Please adjust the workout gradually and include adequate rest."
        )