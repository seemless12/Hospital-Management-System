import sqlite3,json
from fastapi import HTTPException
# Database connection
def get_db():
    conn = sqlite3.connect('patients.db')
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
conn.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    blood_type TEXT NOT NULL,
    contact_phone TEXT NOT NULL,
    contact_email TEXT,
    Medical_History TEXT DEFAULT 'None',
    doctor_assigned TEXT NOT NULL
)''')

conn.commit()

conn.close()

from fastapi import HTTPException
# CRUD Operations
def create_patients(name, age, gender, blood_type, contact_phone, contact_email,Medical_History,doctor_assigned):
    try:
        conn = get_db()
        # This is Becaues Sqlite Does not support List Directly
        if isinstance(Medical_History, list):
            Medical_History = json.dumps(Medical_History)
        
        conn.execute('''
            INSERT INTO patients (name, age, gender, blood_type, contact_phone, contact_email,Medical_History,doctor_assigned)
            VALUES (?, ?, ?, ?, ?, ?,?,?)
        ''', (name, age, gender, blood_type, contact_phone, contact_email,Medical_History,doctor_assigned))
        conn.commit()
        conn.close()
        
        # i added this part becaue i was getting no output in console
        print("✅ Patient inserted successfully.")
        return True
    except Exception as e:
        print(" Database Error:", e)
        raise HTTPException(status_code=500, detail=f"Database error: {e}")



def get_patients():
    conn = get_db()
    quary = conn.execute('''SELECT * FROM patients''')
    rows = quary.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_patient(patient_id, name, age    , gender, blood_type, contact_phone,doctor_assigned):
    conn = get_db()
    quary = conn.execute('''UPDATE patients SET name = ?, age = ?, gender = ?, blood_type = ?,contact_phone = ?,doctor_assigned=?, WHERE id = ?''',  (name, age, gender, blood_type, contact_phone, patient_id,doctor_assigned))
    if quary.rowcount == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    conn.commit()   
    conn.close()   
    return True 

def delete_patient(patient_id):
    
    conn = get_db() 
    quary = conn.execute('''DELETE FROM patients WHERE id = ?''', (patient_id,))
    if quary.rowcount == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    conn.commit()   
    conn.close()
    return True