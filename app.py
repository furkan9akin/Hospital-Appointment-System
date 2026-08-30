from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import AppointmentDB
from datetime import date, datetime
import os
import re


app = Flask(__name__)

# Use an environment variable in production.
# The fallback value is intended only for local development.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-only-secret-key"
)

db = AppointmentDB()


ALLOWED_STATUSES = {
    "scheduled",
    "completed",
    "cancelled",
    "no-show"
}

ALLOWED_DURATIONS = {
    15,
    30,
    45,
    60,
    90,
    120
}


def is_valid_email(email):
    """Return True for an empty email or a basic valid email format."""
    if not email:
        return True

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def parse_appointment_datetime(appointment_date, appointment_time):
    """Convert form date and time values into a datetime object."""
    return datetime.strptime(
        f"{appointment_date} {appointment_time}",
        "%Y-%m-%d %H:%M"
    )


@app.route("/")
def index():
    stats = db.get_appointment_stats()

    today = date.today()
    today_string = today.isoformat()

    today_appointments = db.get_appointments_by_date(today_string)

    all_appointments = db.get_all_appointments()

    upcoming_appointments = [
        appointment
        for appointment in all_appointments
        if str(appointment["appointment_date"]) >= today_string
        and appointment["status"] == "scheduled"
    ][:5]

    return render_template(
        "index.html",
        stats=stats,
        today_appointments=today_appointments,
        upcoming_appointments=upcoming_appointments
    )


@app.route("/about")
def about():
    return render_template("about.html")


# --------------------------------------------------
# Appointment Routes
# --------------------------------------------------

@app.route("/appointments")
def appointments():
    appointments = db.get_all_appointments()

    return render_template(
        "appointments.html",
        appointments=appointments
    )


@app.route("/appointments/add", methods=["GET", "POST"])
def add_appointment():

    if request.method == "POST":

        try:
            patient_id = int(request.form["patient_id"])
            doctor_id = int(request.form["doctor_id"])

            appointment_date = request.form["appointment_date"].strip()
            appointment_time = request.form["appointment_time"].strip()

            duration_minutes = int(
                request.form.get("duration_minutes", 30)
            )

            notes = request.form.get("notes", "").strip()

            if not db.get_patient_by_id(patient_id):
                raise ValueError("Please select a valid patient.")

            if not db.get_doctor_by_id(doctor_id):
                raise ValueError("Please select a valid doctor.")

            if duration_minutes not in ALLOWED_DURATIONS:
                raise ValueError("Please select a valid appointment duration.")

            appointment_datetime = parse_appointment_datetime(
                appointment_date,
                appointment_time
            )

            if appointment_datetime < datetime.now():
                raise ValueError(
                    "Appointments cannot be scheduled in the past."
                )

            db.add_appointment(
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                duration_minutes,
                notes
            )

            flash(
                "Appointment created successfully.",
                "success"
            )

            return redirect(url_for("appointments"))

        except ValueError as error:

            flash(str(error), "error")

        except Exception:

            app.logger.exception(
                "Unexpected error while creating appointment"
            )

            flash(
                "An unexpected error occurred while creating the appointment.",
                "error"
            )

    patients = db.get_all_patients()
    doctors = db.get_all_doctors()

    return render_template(
        "add_appointment.html",
        patients=patients,
        doctors=doctors,
        today=date.today().isoformat()
    )


@app.route(
    "/appointments/<int:appointment_id>/status",
    methods=["POST"]
)
def update_appointment_status(appointment_id):

    try:
        new_status = request.form["status"]
        notes = request.form.get("notes", "").strip()

        if new_status not in ALLOWED_STATUSES:
            raise ValueError("Invalid appointment status.")

        db.update_appointment_status(
            appointment_id,
            new_status,
            notes
        )

        flash(
            "Appointment status updated successfully.",
            "success"
        )

    except ValueError as error:

        flash(str(error), "error")

    except Exception:

        app.logger.exception(
            "Unexpected error while updating appointment status"
        )

        flash(
            "An unexpected error occurred while updating the appointment.",
            "error"
        )

    return redirect(url_for("appointments"))


@app.route(
    "/appointments/<int:appointment_id>/delete",
    methods=["POST"]
)
def delete_appointment(appointment_id):

    try:
        db.delete_appointment(appointment_id)

        flash(
            "Appointment deleted successfully.",
            "success"
        )

    except Exception:

        app.logger.exception(
            "Unexpected error while deleting appointment"
        )

        flash(
            "An unexpected error occurred while deleting the appointment.",
            "error"
        )

    return redirect(url_for("appointments"))


# --------------------------------------------------
# Patient Routes
# --------------------------------------------------

@app.route("/patients")
def patients():

    patients = db.get_all_patients()

    return render_template(
        "patients.html",
        patients=patients
    )


@app.route("/patients/add", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        try:
            first_name = request.form["first_name"].strip()
            last_name = request.form["last_name"].strip()
            phone = request.form["phone"].strip()

            email = request.form.get("email", "").strip()
            date_of_birth = request.form.get(
                "date_of_birth",
                ""
            ).strip()

            address = request.form.get(
                "address",
                ""
            ).strip()

            if not first_name:
                raise ValueError("First name is required.")

            if not last_name:
                raise ValueError("Last name is required.")

            if not phone:
                raise ValueError("Phone number is required.")

            if not is_valid_email(email):
                raise ValueError(
                    "Please enter a valid email address."
                )

            if date_of_birth:
                birth_date = datetime.strptime(
                    date_of_birth,
                    "%Y-%m-%d"
                ).date()

                if birth_date > date.today():
                    raise ValueError(
                        "Date of birth cannot be in the future."
                    )

            db.add_patient(
                first_name,
                last_name,
                phone,
                email,
                date_of_birth,
                address
            )

            flash(
                "Patient added successfully.",
                "success"
            )

            return redirect(url_for("patients"))

        except ValueError as error:

            flash(str(error), "error")

        except Exception:

            app.logger.exception(
                "Unexpected error while adding patient"
            )

            flash(
                "An unexpected error occurred while adding the patient.",
                "error"
            )

    return render_template("add_patient.html")


# --------------------------------------------------
# Doctor Routes
# --------------------------------------------------

@app.route("/doctors")
def doctors():

    doctors = db.get_all_doctors()

    return render_template(
        "doctors.html",
        doctors=doctors
    )


@app.route("/doctors/add", methods=["GET", "POST"])
def add_doctor():

    if request.method == "POST":

        try:
            first_name = request.form["first_name"].strip()
            last_name = request.form["last_name"].strip()
            specialization = request.form[
                "specialization"
            ].strip()

            phone = request.form["phone"].strip()
            email = request.form.get("email", "").strip()

            if not first_name:
                raise ValueError("First name is required.")

            if not last_name:
                raise ValueError("Last name is required.")

            if not specialization:
                raise ValueError("Specialization is required.")

            if not phone:
                raise ValueError("Phone number is required.")

            if not is_valid_email(email):
                raise ValueError(
                    "Please enter a valid email address."
                )

            db.add_doctor(
                first_name,
                last_name,
                specialization,
                phone,
                email
            )

            flash(
                "Doctor added successfully.",
                "success"
            )

            return redirect(url_for("doctors"))

        except ValueError as error:

            flash(str(error), "error")

        except Exception:

            app.logger.exception(
                "Unexpected error while adding doctor"
            )

            flash(
                "An unexpected error occurred while adding the doctor.",
                "error"
            )

    return render_template("add_doctor.html")


# --------------------------------------------------
# API Routes
# --------------------------------------------------

@app.route("/api/appointments/<appointment_date>")
def api_appointments_by_date(appointment_date):

    try:
        # Validate YYYY-MM-DD format.
        datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        )

        appointments = db.get_appointments_by_date(
            appointment_date
        )

        return jsonify(
            [dict(appointment) for appointment in appointments]
        )

    except ValueError:

        return jsonify(
            {"error": "Date must use YYYY-MM-DD format."}
        ), 400

    except Exception:

        app.logger.exception(
            "Unexpected error while retrieving appointments"
        )

        return jsonify(
            {"error": "Unable to retrieve appointments."}
        ), 500


@app.route("/api/stats")
def api_stats():

    try:
        return jsonify(
            db.get_appointment_stats()
        )

    except Exception:

        app.logger.exception(
            "Unexpected error while retrieving statistics"
        )

        return jsonify(
            {"error": "Unable to retrieve statistics."}
        ), 500


if __name__ == "__main__":

    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1"
    )
