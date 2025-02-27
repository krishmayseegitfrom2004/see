from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
import os
import csv
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "secret_key"
DATABASE = "attendance.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create table for students
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        roll_number TEXT,
                        face_id TEXT
                    )''')
    # Create table for attendance
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        time TEXT
                    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    conn.close()
    return render_template("attendance.html", records=records)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get("name")
        roll_number = request.form.get("roll_number")
        face_id = request.form.get("face_id")
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, roll_number, face_id) VALUES (?, ?, ?)",
                       (name, roll_number, face_id))
        conn.commit()
        conn.close()
        flash("User created successfully")
        return redirect(url_for('create_user'))
    return render_template("create_user.html")

@app.route('/download', methods=['GET'])
def download():
    # Retrieve attendance records
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    conn.close()
    
    # Generate CSV file
    csv_file = "attendance.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "User", "Time"])
        writer.writerows(records)
    
    # Generate PDF file
    pdf_file = "attendance.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Attendance Report", ln=True, align='C')
    pdf.ln(10)
    for record in records:
        pdf.cell(200, 10, txt=f"ID: {record[0]}, User: {record[1]}, Time: {record[2]}", ln=True)
    pdf.output(pdf_file)
    
    # For simplicity, send CSV file as download (you could also let users choose)
    return send_file(csv_file, as_attachment=True)

def clear_attendance():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(hours=12)
    cursor.execute("DELETE FROM attendance WHERE datetime(time) < ?", (cutoff.strftime("%Y-%m-%d %H:%M:%S"),))
    conn.commit()
    conn.close()
    print("Cleared attendance records older than 12 hours.")

# Set up a scheduler to run cleanup every hour
scheduler = BackgroundScheduler()
scheduler.add_job(func=clear_attendance, trigger="interval", minutes=60)
scheduler.start()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
