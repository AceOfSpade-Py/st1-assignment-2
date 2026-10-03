def book_appointment(patient_name, practitioner_name, appointment_time):
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }

    print("Appointment Booked")
    print(f"Patient: {appointment['patient']}")
    print(f"Practitioner: {appointment['practitioner']}")
    print(f"Time: {appointment['time']}")

    return appointment
#
# # Example usage
# book_appointment(
#     "Alice Smith",
#     "Dr. John Doe",
#     "2024-07-20 10:00 AM"
# this is the AI Version


# git status
# git add .
# git commit -m "Message"
# git push
# nothing working bruh?