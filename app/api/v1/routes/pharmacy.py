from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.pharmacy import (
    Medicine,
    PharmacySale
)

from app.schemas.pharmacy import (
    MedicineCreate,
    PharmacySaleCreate
)

from app.api.deps import (
    require_hospital_admin
)

from app.models.user import User

router = APIRouter()


# =========================
# CREATE MEDICINE
# =========================

@router.post("/medicines")
def create_medicine(
    payload: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    medicine = Medicine(
        name=payload.name,
        category=payload.category,
        manufacturer=payload.manufacturer,
        supplier=payload.supplier,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        expiry_date=payload.expiry_date
    )

    db.add(medicine)

    db.commit()

    db.refresh(medicine)

    return medicine


# =========================
# GET MEDICINES
# =========================

@router.get("/medicines")
def get_medicines(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(Medicine).all()


# =========================
# SELL MEDICINE
# =========================

@router.post("/sales")
def sell_medicine(
    payload: PharmacySaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    medicine = db.query(Medicine).filter(
        Medicine.id == payload.medicine_id
    ).first()

    if not medicine:

        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    if medicine.quantity < payload.quantity:

        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total_price = (
        medicine.unit_price *
        payload.quantity
    )

    sale = PharmacySale(
        medicine_name=medicine.name,
        quantity=payload.quantity,
        total_price=total_price,
        patient_name=payload.patient_name,
        sold_by=current_user.email
    )

    medicine.quantity -= payload.quantity

    db.add(sale)

    db.commit()

    db.refresh(sale)

    return {
        "message": "Medicine sold",
        "sale": sale
    }


# =========================
# LOW STOCK ALERTS
# =========================

@router.get("/low-stock")
def low_stock_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    medicines = db.query(
        Medicine
    ).filter(
        Medicine.quantity < 10
    ).all()

    return medicines


# =========================
# PHARMACY ANALYTICS
# =========================

@router.get("/analytics")
def pharmacy_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    medicines = db.query(Medicine).all()

    sales = db.query(PharmacySale).all()

    total_inventory_value = sum(
        medicine.quantity *
        medicine.unit_price
        for medicine in medicines
    )

    total_sales = sum(
        sale.total_price
        for sale in sales
    )

    return {

        "total_medicines": len(medicines),

        "total_sales": total_sales,

        "inventory_value": total_inventory_value
    }