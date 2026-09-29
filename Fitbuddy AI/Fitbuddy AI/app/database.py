from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.orm import mapped_column, sessionmaker

from .config import DATABASE_URL


if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }
else:
    connect_args = {}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(100)
    )

    age: Mapped[int] = mapped_column(
        Integer
    )

    weight: Mapped[float] = mapped_column(
        Float
    )

    goal: Mapped[str] = mapped_column(
        String(50)
    )

    intensity: Mapped[str] = mapped_column(
        String(20)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    original_plan: Mapped[str] = mapped_column(
        Text
    )

    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


def init_db():
    Base.metadata.create_all(
        bind=engine
    )


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def save_user(
    db: Session,
    user_id: str,
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
):
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user:
        user.username = username
        user.age = age
        user.weight = weight
        user.goal = goal
        user.intensity = intensity
    else:
        user = User(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )
        db.add(user)

    db.commit()
    db.refresh(user)

    return user


def save_plan(
    db: Session,
    user_id: str,
    original_plan: str,
    nutrition_tip: str
):
    plan = (
        db.query(Plan)
        .filter(Plan.user_id == user_id)
        .first()
    )

    if plan:
        plan.original_plan = original_plan
        plan.updated_plan = None
        plan.feedback = None
        plan.nutrition_tip = nutrition_tip
        plan.updated_at = None
    else:
        plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip
        )
        db.add(plan)

    db.commit()
    db.refresh(plan)

    return plan


def get_user(
    db: Session,
    user_id: str
):
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def get_plan(
    db: Session,
    user_id: str
):
    return (
        db.query(Plan)
        .filter(Plan.user_id == user_id)
        .first()
    )


def update_plan(
    db: Session,
    user_id: str,
    updated_plan: str,
    feedback: str
):
    plan = get_plan(db, user_id)

    if not plan:
        raise ValueError(
            "No workout plan exists for this user."
        )

    plan.updated_plan = updated_plan
    plan.feedback = feedback
    plan.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(plan)

    return plan


def get_all_users(
    db: Session
):
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )