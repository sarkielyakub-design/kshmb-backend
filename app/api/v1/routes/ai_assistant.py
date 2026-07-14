from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.ai_assistant import (
    AIConsultation
)

from app.schemas.ai_assistant import (
    AIConsultationCreate
)

from app.services.ai_service import (
    analyze_symptoms
)

router = APIRouter()


# =========================
# AI CONSULTATION
# =========================

@router.post("/consult")
def ai_consultation(
    payload: AIConsultationCreate,
    db: Session = Depends(get_db)
):

    result = analyze_symptoms(
        payload.symptoms
    )

    consultation = AIConsultation(
        symptoms=payload.symptoms,
        ai_response=result["ai_response"],
        risk_level=result["risk_level"],
        recommendation=result["recommendation"]
    )

    db.add(consultation)

    db.commit()

    db.refresh(consultation)

    return {

        "medical_disclaimer":
        "This AI system does not replace professional medical advice.",

        "consultation": consultation
    }


# =========================
# GET AI CONSULTATIONS
# =========================

@router.get("/")
def get_ai_consultations(
    db: Session = Depends(get_db)
):

    return db.query(
        AIConsultation
    ).all()