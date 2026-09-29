from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import (
    get_db,
    get_all_users,
    get_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .gemini_generator import (
    generate_workout_gemini
)

from .schemas import (
    FeedbackRequest,
    UserInput
)

from .updated_plan import (
    update_workout_plan
)


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ---------------- HOME PAGE ----------------

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ---------------- GENERATE WORKOUT ----------------

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):

    user_data = UserInput(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    try:

        workout_plan = generate_workout_gemini(
            user_data.username,
            user_data.age,
            user_data.weight,
            user_data.goal,
            user_data.intensity
        )

        nutrition_tip = generate_nutrition_tip_with_flash(
            user_data.goal
        )

    except Exception:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": "Gemini is temporarily unavailable. Please try again shortly."
            }
        )

    save_user(
        db=db,
        user_id=user_data.user_id,
        username=user_data.username,
        age=user_data.age,
        weight=user_data.weight,
        goal=user_data.goal,
        intensity=user_data.intensity
    )

    save_plan(
        db=db,
        user_id=user_data.user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user_data,
            "plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }
    )


# ---------------- SUBMIT FEEDBACK ----------------

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):

    feedback_data = FeedbackRequest(
        user_id=user_id,
        feedback=feedback
    )

    user = get_user(
        db,
        feedback_data.user_id
    )

    plan = get_plan(
        db,
        feedback_data.user_id
    )

    if not user or not plan:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "error": "User or workout plan not found.",
                "plan": "",
                "nutrition_tip": ""
            }
        )

    original_plan = (
        plan.updated_plan
        or plan.original_plan
    )

    try:

        revised_plan = update_workout_plan(
            original_plan=original_plan,
            feedback=feedback_data.feedback,
            goal=user.goal,
            intensity=user.intensity
        )

    except Exception:

        revised_plan = (
            original_plan
            + "\n\nUpdated based on your feedback:\n"
            + feedback_data.feedback
        )

    update_plan(
        db=db,
        user_id=feedback_data.user_id,
        updated_plan=revised_plan,
        feedback=feedback_data.feedback
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "plan": revised_plan,
            "nutrition_tip": plan.nutrition_tip,
            "feedback": feedback_data.feedback
        }
    )


# ---------------- VIEW ALL USERS ----------------

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
async def view_all_users(
    request: Request,
    db: Session = Depends(get_db)
):

    users = get_all_users(db)

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users
        }
    )