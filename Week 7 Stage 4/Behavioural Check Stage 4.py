from datetime import date, time


patient = Patient(
    identifier="P001",
    name="Alex Morgan",
)

practitioner = Practitioner(
    identifier="PR001",
    name="Dr Taylor",
    specialty="General Practice",
)

appointment = Appointment(
    identifier="A001",
    patient=patient,
    practitioner=practitioner,
    appointment_date=date(2026, 10, 3),
    start_time=time(10, 0),
    duration_minutes=30,
)

assert appointment.status is AppointmentStatus.SCHEDULED

appointment.cancel()

assert appointment.status is AppointmentStatus.CANCELLED
assert appointment.patient is patient
assert appointment.practitioner is practitioner

try:
    Patient(identifier="", name="Alex Morgan")
    raise AssertionError("Empty patient identifier should fail.")
except ValueError:
    pass

try:
    Practitioner(
        identifier="PR002",
        name="Dr Lee",
        specialty="",
    )
    raise AssertionError("Empty specialty should fail.")
except ValueError:
    pass

try:
    Appointment(
        identifier="A002",
        patient=patient,
        practitioner=practitioner,
        appointment_date=date(2026, 10, 3),
        start_time=time(11, 0),
        duration_minutes=0,
    )
    raise AssertionError("Zero duration should fail.")
except ValueError:
    pass

try:
    appointment.cancel()
    raise AssertionError("Repeated cancellation should fail.")
except InvalidAppointmentTransitionError:
    pass