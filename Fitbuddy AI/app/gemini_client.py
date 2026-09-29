from google import genai
from .config import GEMINI_API_KEY


def get_client():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "Gemini API key is missing. "
            "Add GEMINI_API_KEY to your .env file."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(model: str, prompt: str, max_output_tokens: int = 4000):
    client = get_client()

    models_to_try = [
        model,
        "gemini-3.5-flash",
        "gemini-3.6-flash"
    ]

    last_error = None

    for current_model in models_to_try:
        try:
            response = client.models.generate_content(
                model=current_model,
                contents=prompt,
                config={
                    "temperature": 0.7,
                    "max_output_tokens": max_output_tokens
                }
            )

            text = getattr(response, "text", None)

            if text:
                return text.strip()

        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(
        f"Gemini could not generate a response. Last error: {last_error}"
    )