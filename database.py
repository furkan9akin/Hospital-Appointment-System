import sqlite3
from datetime import datetime, timedelta

class AppointmentDB:
    def __init__(self, db_name='appointments.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return conn
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                date_of_birth DATE,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                duration_minutes INTEGER DEFAULT 30,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        # Create appointment_status table for tracking status changes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointment_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (appointment_id) REFERENCES appointments (id)
            )
        ''')
        

        
        conn.commit()
        conn.close()
        
        # Insert sample data if tables are empty
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM patients")
        if cursor.fetchone()[0] == 0:
            # Insert sample patients
            patients = [
    (
        "Alex",
        "Morgan",
        "+1-555-0101",
        "alex.morgan@example.test",
        "1985-03-15",
        "Demo City"
    ),
    (
        "Jordan",
        "Lee",
        "+1-555-0102",
        "jordan.lee@example.test",
        "1990-07-22",
        "Demo City"
    )
]
            
            cursor.executemany('''
                INSERT INTO patients (first_name, last_name, phone, email, date_of_birth, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', patients)
            
            # Insert sample doctors
           doctors = [
    (
        "Ahmet",
        "Stone",
        "Cardiology",
        "+1-555-0201",
        "emma.stone@example.test"
    ),
    (
        "Mehmet",
        "Oz",
        "Dermatology",
        "+1-555-0202",
        "daniel.reed@example.test"
    )
]
            
            cursor.executemany('''
                INSERT INTO doctors (first_name, last_name, specialization, phone, email)
                VALUES (?, ?, ?, ?, ?)
            ''', doctors)
            
            # Insert sample appointments
            today = datetime.now().date()
            appointments = [
                (1, 1, today + timedelta(days=1), '09:00', 30, 'scheduled', 'Routine check-up'),
                (2, 2, today + timedelta(days=2), '14:30', 45, 'scheduled', 'Initial consultation'),
                (3, 3, today + timedelta(days=3), '11:00', 60, 'scheduled', 'Post-treatment follow-up'),
                (4, 4, today + timedelta(days=1), '16:00', 30, 'scheduled', 'Eye Diagnosis'),
                (5, 5, today + timedelta(days=4), '10:30', 45, 'scheduled', 'Neurology Diagnosis')
            ]
            
            cursor.executemany('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, duration_minutes, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', appointments)
            
            conn.commit()
        
        conn.close()
    
    # Patient operations
    def add_patient(self, first_name, last_name, phone, email=None, date_of_birth=None, address=None):
        """Add a new patient"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, phone, email, date_of_birth, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, phone, email, date_of_birth, address))
        
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return patient_id
    
    def get_all_patients(self):
        """Get all patients"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients ORDER BY last_name, first_name')
        patients = cursor.fetchall()
        
        conn.close()
        return patients
    
    def get_patient_by_id(self, patient_id):
        """Get patient by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = cursor.fetchone()
        
        conn.close()
        return patient
    
    # Doctor operations
    def add_doctor(self, first_name, last_name, specialization, phone, email=None):
        """Add a new doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO doctors (first_name, last_name, specialization, phone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, specialization, phone, email))
        
        doctor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return doctor_id
    
    def get_all_doctors(self):
        """Get all doctors"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM doctors ORDER BY last_name, first_name')
        doctors = cursor.fetchall()
        
        conn.close()
        return doctors
    
    def get_doctor_by_id(self, doctor_id):
        """Get doctor by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM doctors WHERE id = ?', (doctor_id,))
        doctor = cursor.fetchone()
        
        conn.close()
        return doctor
    
    # Appointment operations
    def add_appointment(self, patient_id, doctor_id, appointment_date, appointment_time, duration_minutes=30, notes=None):
        """Add a new appointment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, duration_minutes, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_id, doctor_id, appointment_date, appointment_time, duration_minutes, notes))
        
        appointment_id = cursor.lastrowid
        
        # Add initial status
        cursor.execute('''
            INSERT INTO appointment_status (appointment_id, status, notes)
            VALUES (?, ?, ?)
        ''', (appointment_id, 'scheduled', 'Appointment created'))
        
        conn.commit()
        conn.close()
        return appointment_id
    
    def get_all_appointments(self):
        """Get all appointments with patient and doctor details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                a.id,
                a.appointment_date,
                a.appointment_time,
                a.duration_minutes,
                a.status,
                a.notes,
                p.first_name as patient_first_name,
                p.last_name as patient_last_name,
                p.phone as patient_phone,
                d.first_name as doctor_first_name,
                d.last_name as doctor_last_name,
                d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date, a.appointment_time
        ''')
        
        appointments = cursor.fetchall()
        conn.close()
        return appointments
    
    def get_appointments_by_date(self, date):
        """Get appointments for a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                a.id,
                a.appointment_date,
                a.appointment_time,
                a.duration_minutes,
                a.status,
                a.notes,
                p.first_name as patient_first_name,
                p.last_name as patient_last_name,
                p.phone as patient_phone,
                d.first_name as doctor_first_name,
                d.last_name as doctor_last_name,
                d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.appointment_date = ?
            ORDER BY a.appointment_time
        ''', (date,))
        
        appointments = cursor.fetchall()
        conn.close()
        return appointments
    
    def update_appointment_status(self, appointment_id, new_status, notes=None):
        """Update appointment status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Update appointment status
        cursor.execute('''
            UPDATE appointments SET status = ? WHERE id = ?
        ''', (new_status, appointment_id))
        
        # Add status change record
        cursor.execute('''
            INSERT INTO appointment_status (appointment_id, status, notes)
            VALUES (?, ?, ?)
        ''', (appointment_id, new_status, notes))
        
        conn.commit()
        conn.close()
    
    def delete_appointment(self, appointment_id):
        """Delete an appointment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete status records first
        cursor.execute('DELETE FROM appointment_status WHERE appointment_id = ?', (appointment_id,))
        
        # Delete appointment
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        
        conn.commit()
        conn.close()
    
    def get_appointment_stats(self):
        """Get appointment statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total appointments
        cursor.execute('SELECT COUNT(*) FROM appointments')
        total_appointments = cursor.fetchone()[0]
        
        # Appointments by status
        cursor.execute('''
            SELECT status, COUNT(*) as count 
            FROM appointments 
            GROUP BY status
        ''')
        status_counts = cursor.fetchall()
        
        # Today's appointments
        today = datetime.now().date()
        cursor.execute('SELECT COUNT(*) FROM appointments WHERE appointment_date = ?', (today,))
        today_appointments = cursor.fetchone()[0]
        
        # This week's appointments
        week_start = today - timedelta(days=today.weekday())
        cursor.execute('''
            SELECT COUNT(*) FROM appointments 
            WHERE appointment_date BETWEEN ? AND ?
        ''', (week_start, week_start + timedelta(days=6)))
        week_appointments = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total_appointments,
            'status_counts': status_counts,
            'today': today_appointments,
            'this_week': week_appointments
        }
    
if __name__ == "__main__":
    AppointmentDB()
