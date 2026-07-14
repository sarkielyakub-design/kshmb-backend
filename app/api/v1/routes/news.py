from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from slugify import slugify

from app.db.session import get_db

from app.models.news import News

from app.schemas.news import (
    NewsCreate,
    NewsUpdate,
    NewsResponse
)

from app.api.deps import (
    require_super_admin
)

router = APIRouter()


# =====================================
# CREATE NEWS
# =====================================

@router.post(
    "/",
    response_model=NewsResponse,
    status_code=status.HTTP_201_CREATED
)
def create_news(
    payload: NewsCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_super_admin
    )
):

    slug = slugify(payload.title)

    existing = db.query(
        News
    ).filter(
        News.slug == slug
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="News already exists"
        )

    news = News(

        title=payload.title,

        slug=slug,

        summary=payload.summary,

        content=payload.content,

        image=payload.image,

        author=payload.author,

        headline=payload.headline
    )

    db.add(news)

    db.commit()

    db.refresh(news)

    return news


# =====================================
# GET ALL NEWS
# =====================================

@router.get(
    "/",
    response_model=list[NewsResponse]
)
def get_news(
    db: Session = Depends(get_db)
):

    return db.query(
        News
    ).filter(
        News.published == True
    ).order_by(
        News.created_at.desc()
    ).all()


# =====================================
# HEADLINES
# =====================================

@router.get(
    "/headlines",
    response_model=list[NewsResponse]
)
def get_headlines(
    db: Session = Depends(get_db)
):

    return db.query(
        News
    ).filter(
        News.headline == True,
        News.published == True
    ).order_by(
        News.created_at.desc()
    ).limit(10).all()


# =====================================
# SINGLE NEWS
# =====================================

@router.get(
    "/{slug}",
    response_model=NewsResponse
)
def get_single_news(
    slug: str,
    db: Session = Depends(get_db)
):

    news = db.query(
        News
    ).filter(
        News.slug == slug
    ).first()

    if not news:

        raise HTTPException(
            status_code=404,
            detail="News not found"
        )

    return news