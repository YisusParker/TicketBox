import enum
from datetime import datetime
from datetime import UTC

from sqlalchemy import String, DateTime, Integer, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EventStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    cancelled = "cancelled"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    venue: Mapped[str] = mapped_column(String(255), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus), default=EventStatus.draft, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
