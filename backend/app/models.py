from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

feedback_tag = Table(
    "feedback_tag",
    Base.metadata,
    Column(
        "feedback_id",
        String,
        ForeignKey("feedback.id", ondelete="RESTRICT"),
        primary_key=True,
    ),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="RESTRICT"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    def to_dict(self) -> dict:
        return {"name": self.name}


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[list[Tag]] = relationship(secondary=feedback_tag, lazy="selectin")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "tags": [t.name for t in self.tags],
            "created_at": self.created_at.isoformat(),
            "is_archived": self.is_archived,
        }
