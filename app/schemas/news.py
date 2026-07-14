from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =====================================
# CREATE
# =====================================

class NewsCreate(BaseModel):

    title: str

    summary: Optional[str] = None

    content: str

    image: Optional[str] = None

    author: Optional[str] = None

    headline: bool = False


# =====================================
# UPDATE
# =====================================

class NewsUpdate(BaseModel):

    title: Optional[str] = None

    summary: Optional[str] = None

    content: Optional[str] = None

    image: Optional[str] = None

    author: Optional[str] = None

    headline: Optional[bool] = None

    published: Optional[bool] = None


# =====================================
# RESPONSE
# =====================================

class NewsResponse(BaseModel):

    id: int

    title: str

    slug: str

    summary: Optional[str]

    content: str

    image: Optional[str]

    author: Optional[str]

    headline: bool

    published: bool

    created_at: datetime

    class Config:

        from_attributes = True