from pydantic import BaseModel


class AIConsultationCreate(BaseModel):

    symptoms: str