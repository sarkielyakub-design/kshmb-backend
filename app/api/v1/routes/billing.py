from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.billing import (
    Invoice
)

from app.models.patient import (
    Patient
)

from app.schemas.billing import (
    InvoiceCreate,
    PaymentStatusUpdate
)

from app.api.deps import (
    require_hospital_admin,
    require_super_admin
)

from app.models.user import User

import uuid

router = APIRouter()


# =========================
# CREATE INVOICE
# =========================

@router.post("/")
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    patient = db.query(Patient).filter(
        Patient.id == payload.patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    invoice = Invoice(
        patient_id=payload.patient_id,
        service_name=payload.service_name,
        amount=payload.amount,
        payment_method=payload.payment_method,
        invoice_number=str(uuid.uuid4())[:8]
    )

    db.add(invoice)

    db.commit()

    db.refresh(invoice)

    return {
        "message": "Invoice created",
        "invoice": invoice
    }


# =========================
# GET INVOICES
# =========================

@router.get("/")
def get_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(Invoice).all()


# =========================
# UPDATE PAYMENT STATUS
# =========================

@router.patch("/{invoice_id}/status")
def update_payment_status(
    invoice_id: int,
    payload: PaymentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_super_admin
    )
):

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:

        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    invoice.payment_status = payload.payment_status

    db.commit()

    db.refresh(invoice)

    return {
        "message": "Payment updated",
        "invoice": invoice
    }


# =========================
# FINANCIAL ANALYTICS
# =========================

@router.get("/analytics")
def billing_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_super_admin
    )
):

    invoices = db.query(Invoice).all()

    total_revenue = sum(
        invoice.amount
        for invoice in invoices
        if invoice.payment_status == "PAID"
    )

    unpaid_revenue = sum(
        invoice.amount
        for invoice in invoices
        if invoice.payment_status == "UNPAID"
    )

    return {

        "total_invoices": len(invoices),

        "paid_revenue": total_revenue,

        "unpaid_revenue": unpaid_revenue
    }