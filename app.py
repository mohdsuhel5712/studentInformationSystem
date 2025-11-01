from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

# ---------- ROUTES ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return render_template('view.html', students=data)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    conn = sqlite3.connect('students.db')
    conn.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
                 (name, email, course))
    conn.commit()
    conn.close()
    return redirect(url_for('view'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        cursor.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?",
                       (name, email, course, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view'))
    else:
        cursor.execute("SELECT * FROM students WHERE id=?", (id,))
        student = cursor.fetchone()
        conn.close()
        return render_template('update.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view'))

if __name__ == '__main__':
    app.run(debug=True)
 