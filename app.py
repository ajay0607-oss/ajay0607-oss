from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='pokemon',
        database='student_management'
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Hardcoded admin login
        if email == 'admin@example.com' and password == 'admin123' and role == 'admin':
            session['user_id'] = 'admin'
            session['role'] = 'admin'
            session['name'] = 'Admin'
            flash('Admin login successful!', 'success')
            return redirect(url_for('dashboard'))

        # Check user from database
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s AND is_approved = TRUE",
            (email, password, role)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials or not approved.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        mobile = request.form['mobile']

        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, role, mobile) VALUES (%s, %s, %s, %s, %s)",
                (name, email, password, role, mobile)
            )
            db.commit()
            flash('Registration successful! Awaiting approval.', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    role = session.get('role')
    name = session.get('name')

    # Fetch announcements for students and faculty
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    announcements = cursor.fetchall()
    cursor.close()
    db.close()

    if role == 'admin':
        return render_template('admin_dashboard.html', name=name)
    elif role == 'faculty':
        return render_template('faculty_dashboard.html', name=name, announcements=announcements)
    else:
        return render_template('student_dashboard.html', name=name, announcements=announcements)
        return render_template('student_dashboard.html', name=name, announcements=announcements)

@app.route('/approve_users', methods=['GET', 'POST'])
def approve_users():
    if 'user_id' not in session or session.get('role') not in ['admin', 'faculty']:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Faculty can only see students pending approval, Admin can see all
    if session.get('role') == 'faculty':
        cursor.execute("SELECT * FROM users WHERE is_approved = FALSE AND role = 'student'")
    else:
        cursor.execute("SELECT * FROM users WHERE is_approved = FALSE")

    users = cursor.fetchall()

    if request.method == 'POST':
        user_id = request.form['user_id']
        cursor.execute("UPDATE users SET is_approved = TRUE WHERE id = %s", (user_id,))
        db.commit()
        flash('User approved successfully!', 'success')

    cursor.close()
    db.close()
    return render_template('approve_users.html', users=users)

@app.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Logic to handle file upload (not implemented here)
        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('upload_document.html')

@app.route('/announce', methods=['GET', 'POST'])
def announce():
    if 'user_id' not in session or session.get('role') not in ['admin', 'faculty']:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        message = request.form.get('message')
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO announcements (message) VALUES (%s)", (message,))
        db.commit()
        cursor.close()
        db.close()
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('announce.html')

@app.route('/faculty_links')
def faculty_links():
    # Static list of faculty names with their external profile links
    faculties = [
        {'name': 'Dr. Sanjay Kumar', 'link': 'https://www.prsu.ac.in/site/facultydetails?id=994'},
        {'name': 'Dr. V.K.Patle', 'link': 'https://www.prsu.ac.in/site/facultydetails?id=44'},
        {'name': 'Deepak Kumar Deshmukh', 'link': 'https://www.prsu.ac.in/site/facultydetails?id=46'},
        {'name': 'Rahul Kumar Singh', 'link': 'https://www.prsu.ac.in/site/facultydetails?id=182'},
        {'name': 'Harsha Pandey', 'link': 'https://www.prsu.ac.in/site/facultydetails?id=983'},
        {'name': 'Ranu Sao', 'link': 'https://www.prsu.ac.in/site/facultydetails?id=985'}
    ]
    return render_template('faculty_links.html', faculties=faculties)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
