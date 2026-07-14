from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.db.session import Base


class AIConsultation(Base):

    __tablename__ = "ai_consultations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    symptoms = Column(Text)

    ai_response = Column(Text)

    risk_level = Column(String)

    recommendation = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )