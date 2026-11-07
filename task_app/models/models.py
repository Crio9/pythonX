from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from task_app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (CheckConstraint("priority BETWEEN 1 AND 5"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)

    priority: Mapped[int] = mapped_column(nullable=False, default=3)

