from sqlalchemy.orm import declarative_base

Base = declarative_base()

# =====================================
# IMPORT ALL MODELS
# =====================================

from app.models.user import User
from app.models.hospital import Hospital
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.staff import Staff
from app.models.bedspace import BedSpace
from app.models.news import News