from datetime import date

from sqlalchemy import Boolean, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
