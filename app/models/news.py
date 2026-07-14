from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
)

from sqlalchemy.sql import func

from app.db.base_class import Base


class News(Base):

    __tablename__ = "news"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    slug = Column(
        String,
        unique=True,
        nullable=False
    )

    headline = Column(
        Boolean,
        default=False
    )

    summary = Column(
        Text,
        nullable=True
    )

    content = Column(
        Text,
        nullable=False
    )

    image = Column(
        String,
        nullable=True
    )

    author = Column(
        String,
        nullable=True
    )

    published = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )