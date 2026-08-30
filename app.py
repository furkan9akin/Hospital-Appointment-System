from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import AppointmentDB
from datetime import date
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Initialize database
db = AppointmentDB()

@app.route('/')
def index():
    # Get statistics for dashboard
    stats = db.get_appointment_stats()
    
    # Get today's appointments
    today = date.today()
    today_appointments = db.get_appointments_by_date(today)
    
    # Get upcoming appointments (next 7 days)
    upcoming_appointments = db.get_all_appointments()
    
    return render_template('index.html', 
                         stats=stats, 
                         today_appointments=today_appointments,
                         upcoming_appointments=upcoming_appointments[:5])  # Show only first 5

@app.route('/about')
def about():
    return render_template('about.html')

# Appointment routes
@app.route('/appointments')
def appointments():
    appointments = db.get_all_appointments()
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        try:
            patient_id = int(request.form['patient_id'])
            doctor_id = int(request.form['doctor_id'])
            appointment_date = request.form['appointment_date']
            appointment_time = request.form['appointment_time']
            duration_minutes = int(request.form.get('duration_minutes', 30))
            notes = request.form.get('notes', '')
            
            db.add_appointment(patient_id, doctor_id, appointment_date, appointment_time, duration_minutes, notes)
            flash('Randevu başarıyla eklendi!', 'success')
            return redirect(url_for('appointments'))
        except Exception as e:
            flash(f'Randevu eklenirken hata oluştu: {str(e)}', 'error')
    
    patients = db.get_all_patients()
    doctors = db.get_all_doctors()
    return render_template('add_appointment.html', patients=patients, doctors=doctors)

@app.route('/appointments/<int:appointment_id>/status', methods=['POST'])
def update_appointment_status(appointment_id):
    try:
        new_status = request.form['status']
        notes = request.form.get('notes', '')
        db.update_appointment_status(appointment_id, new_status, notes)
        flash('Randevu durumu güncellendi!', 'success')
    except Exception as e:
        flash(f'Durum güncellenirken hata oluştu: {str(e)}', 'error')
    
    return redirect(url_for('appointments'))

@app.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def delete_appointment(appointment_id):
    try:
        db.delete_appointment(appointment_id)
        flash('Randevu silindi!', 'success')
    except Exception as e:
        flash(f'Randevu silinirken hata oluştu: {str(e)}', 'error')
    
    return redirect(url_for('appointments'))

# Patient routes
@app.route('/patients')
def patients():
    patients = db.get_all_patients()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone = request.form['phone']
            email = request.form.get('email', '')
            date_of_birth = request.form.get('date_of_birth', '')
            address = request.form.get('address', '')
            
            db.add_patient(first_name, last_name, phone, email, date_of_birth, address)
            flash('Hasta başarıyla eklendi!', 'success')
            return redirect(url_for('patients'))
        except Exception as e:
            flash(f'Hasta eklenirken hata oluştu: {str(e)}', 'error')
    
    return render_template('add_patient.html')

# Doctor routes
@app.route('/doctors')
def doctors():
    doctors = db.get_all_doctors()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            specialization = request.form['specialization']
            phone = request.form['phone']
            email = request.form.get('email', '')
            
            db.add_doctor(first_name, last_name, specialization, phone, email)
            flash('Doktor başarıyla eklendi!', 'success')
            return redirect(url_for('doctors'))
        except Exception as e:
            flash(f'Doktor eklenirken hata oluştu: {str(e)}', 'error')
    
    return render_template('add_doctor.html')

# API routes for AJAX requests
@app.route('/api/appointments/<date>')
def api_appointments_by_date(date):
    try:
        appointments = db.get_appointments_by_date(date)
        return jsonify([dict(appointment) for appointment in appointments])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/stats')
def api_stats():
    try:
        stats = db.get_appointment_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
