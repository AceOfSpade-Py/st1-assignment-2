from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional


# --- Enum ---

class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


# --- Exception ---

class InvalidTransitionError(ValueError):
    pass


# --- Domain ---

@dataclass(frozen=True)
class Patient:
    identifier: str
    name: str

    def __post_init__(self):
        if not self.identifier.strip():
            raise ValueError("Patient identifier cannot be empty.")
        if not self.name.strip():
            raise ValueError("Patient name cannot be empty.")


@dataclass(frozen=True)
class Practitioner:
    identifier: str
    name: str
    specialty: str

    def __post_init__(self):
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

    def __post_init__(self):
        if not self.identifier.strip():
            raise ValueError("Appointment identifier cannot be empty.")
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be greater than zero.")

    def cancel(self):
        if self.status is AppointmentStatus.CANCELLED:
            raise InvalidTransitionError("Already cancelled.")
        self.status = AppointmentStatus.CANCELLED

    def overlaps(self, other: "Appointment") -> bool:
        if self.appointment_date != other.appointment_date:
            return False
        s1 = self.start_time.hour * 60 + self.start_time.minute
        e1 = s1 + self.duration_minutes
        s2 = other.start_time.hour * 60 + other.start_time.minute
        e2 = s2 + other.duration_minutes
        return s1 < e2 and s2 < e1


# --- Repository ---

class AppointmentRepository(ABC):
    @abstractmethod
    def save(self, appointment: Appointment) -> None: ...

    @abstractmethod
    def find_by_id(self, identifier: str) -> Optional[Appointment]: ...

    @abstractmethod
    def find_by_practitioner(self, practitioner_id: str) -> list: ...


class InMemoryAppointmentRepository(AppointmentRepository):
    def __init__(self):
        self._store: dict = {}

    def save(self, appointment: Appointment) -> None:
        self._store[appointment.identifier] = appointment

    def find_by_id(self, identifier: str) -> Optional[Appointment]:
        return self._store.get(identifier)

    def find_by_practitioner(self, practitioner_id: str) -> list:
        return [a for a in self._store.values()
                if a.practitioner.identifier == practitioner_id]


# --- Service ---

class AppointmentService:
    def __init__(self, repository: AppointmentRepository):
        self._repository = repository

    def book(self, identifier, patient, practitioner,
             appointment_date, start_time, duration_minutes):
        new = Appointment(identifier, patient, practitioner,
                          appointment_date, start_time, duration_minutes)
        for existing in self._repository.find_by_practitioner(practitioner.identifier):
            if existing.status is AppointmentStatus.CANCELLED:
                continue
            if new.overlaps(existing):
                raise ValueError("Conflicting appointment exists.")
        self._repository.save(new)
        return new

    def cancel(self, identifier: str):
        appt = self._repository.find_by_id(identifier)
        if appt is None:
            raise ValueError(f"Appointment {identifier} not found.")
        appt.cancel()
        self._repository.save(appt)


# --- Verification ---

if __name__ == "__main__":
    repo = InMemoryAppointmentRepository()
    service = AppointmentService(repo)

    p = Patient("P001", "Alex Morgan")
    pr = Practitioner("PR001", "Dr Taylor", "General Practice")

    a1 = service.book("A001", p, pr, date(2026, 10, 3), time(10, 0), 30)
    assert a1.status is AppointmentStatus.SCHEDULED

    try:
        service.book("A002", p, pr, date(2026, 10, 3), time(10, 15), 30)
        assert False, "Overlap should fail."
    except ValueError:
        pass

    service.cancel("A001")
    assert repo.find_by_id("A001").status is AppointmentStatus.CANCELLED

    try:
        service.cancel("A001")
        assert False, "Repeated cancel should fail."
    except InvalidTransitionError:
        pass

    try:
        Patient("", "Alex")
        assert False
    except ValueError:
        pass

    print("All checks passed.")