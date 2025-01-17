from flask import Flask, render_template, send_file, request, redirect, url_for
from pathlib import Path
import sqlite3
import os

app = Flask(__name__)

# Database setup
os.makedirs("database", exist_ok=True)

# Connect to the database and create the table if it doesn't exist
con = sqlite3.connect("database/form.db", check_same_thread=False)
con.execute("CREATE TABLE IF NOT EXISTS User (name TEXT, email TEXT, subject TEXT, message TEXT)")
con.commit()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handling form submission
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Insert data into the database
        con = sqlite3.connect("database/form.db")
        con.execute("INSERT INTO User (name, email, subject, message) VALUES (?, ?, ?, ?)", 
                    (name, email, subject, message))
        con.commit()

        # Redirect to the same page after submission
        return redirect(url_for('home'))

    # If GET request, just render the home page
    return render_template('index.html')

@app.route('/download-resume')
def download_resume():
    # Assuming resume.pdf is stored in 'static/img' directory
    resume_path = Path(__file__).parent / 'static' / 'img' / 'resume.pdf'
    return send_file(resume_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
