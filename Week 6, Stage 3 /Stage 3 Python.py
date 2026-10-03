from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from typing import Optional


class AppointmentStatus(Enum):
    BOOKED = "booked"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


@dataclass
class Patient:
    patient_id: str
    name: str
    date_of_birth: date
    contact_details: str


@dataclass
class Practitioner:
    practitioner_id: str
    name: str
    role: str
    availability: str
    active: bool = True


@dataclass
class Appointment:
    appointment_id: str
    patient: Patient
    practitioner: Practitioner
    appointment_date: date
    start_time: time
    duration_minutes: int
    status: AppointmentStatus = AppointmentStatus.BOOKED