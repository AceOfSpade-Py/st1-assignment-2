from dataclasses import dataclass
from datetime import date, time
from enum import Enum


class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


class InvalidAppointmentTransitionError(ValueError):
    """Raised when an appointment status change is not permitted."""


@dataclass(frozen=True)
class Patient:
    identifier: str
    name: str

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("Patient identifier cannot be empty.")
        if not self.name.strip():
            raise ValueError("Patient name cannot be empty.")


@dataclass(frozen=True)
class Practitioner:
    identifier: str
    name: str
    specialty: str

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("Practitioner identifier cannot be empty.")
        if not self.name.strip():
            raise ValueError("Practitioner name cannot be empty.")
        if not self.specialty.strip():
            raise ValueError("Practitioner specialty cannot be empty.")


@dataclass
class Appointment:
    identifier: str
    patient: Patient
    practitioner: Practitioner
    appointment_date: date
    start_time: time
    duration_minutes: int
    status: AppointmentStatus = AppointmentStatus.SCHEDULED

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("Appointment identifier cannot be empty.")
        if self.duration_minutes <= 0:
            raise ValueError("Appointment duration must be greater than zero.")

    def cancel(self) -> None:
        if self.status is AppointmentStatus.CANCELLED:
            raise InvalidAppointmentTransitionError(
                "A cancelled appointment cannot be cancelled again."
            )

        self.status = AppointmentStatus.CANCELLED