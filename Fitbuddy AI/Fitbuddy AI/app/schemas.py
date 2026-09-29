from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):

    username: str = Field(
        min_length=1,
        max_length=100
    )

    user_id: str = Field(
        min_length=1,
        max_length=50
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=20,
        lt=500
    )

    goal: str

    intensity: str

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value: str):

        allowed = {
            "weight loss",
            "muscle gain",
            "general wellness",
            "flexibility"
        }

        value = value.strip().lower()

        if value not in allowed:
            raise ValueError(
                "Invalid fitness goal."
            )

        return value

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value: str):

        value = value.strip().lower()

        if value not in {
            "low",
            "medium",
            "high"
        }:
            raise ValueError(
                "Intensity must be low, medium, or high."
            )

        return value


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=1,
        max_length=50
    )

    feedback: str = Field(
        min_length=3,
        max_length=1000
    )