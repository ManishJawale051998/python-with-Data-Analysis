from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create table
@app.route('/create')
def create():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            science INTEGER,
            maths INTEGER,
            english INTEGER,
            history INTEGER,
            obtained_marks INTEGER,
            percentage REAL,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()
    return "Table created successfully"


@app.route('/delete')
def delete():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('delete from marks')
    conn.commit()
    conn.close()
    return "Records deleted successfully"


@app.route('/insert_student', methods=['POST'])
def insert_student():
    data = request.get_json()
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    for student in data:
        cursor.execute('''
               INSERT INTO marks (id, name, science, maths, english, history, obtained_marks, percentage, grade)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ''', (
            student.get('id'),
            student.get('name'),
            student.get('science'),
            student.get('maths'),
            student.get('english'),
            student.get('history'),
            student.get('obtained_marks'),
            student.get('percentage'),
            student.get('grade')
        ))
    conn.commit()
    conn.close()
    return "Student added successfully"


@app.route('/update_marks', methods=['POST'])
def update_marks():
    data = request.get_json()
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()


    obtained_marks = sum([
        data.get('science', 0),
        data.get('maths', 0),
        data.get('english', 0),
        data.get('history', 0)
    ])
    percentage = (obtained_marks / 400) * 100

    # Assign grade
    if percentage > 75:
        grade = 'O'
    elif 60 <= percentage <= 75:
        grade = 'A'
    elif 50 <= percentage < 60:
        grade = 'B'
    elif 40 <= percentage < 50:
        grade = 'C'
    else:
        grade = 'F'

    cursor.execute('''
        UPDATE marks
        SET science = ?, maths = ?, english = ?, history = ?,obtained_marks = ?, percentage = ?, grade = ?
        WHERE id = ?
    ''', (data['science'],data['maths'],data['english'],data['history'],obtained_marks, percentage, grade, data['id']))

    conn.commit()
    conn.close()
    return "Marks updated successfully"


@app.route('/getallmarks', methods=['GET'])
def getallmarks():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM marks')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/getstudentmarks', methods=['POST'])
def getstudentmarks():
    data = request.get_json()
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM marks WHERE id = ?', (data['id'],))
    row = cursor.fetchone()
    conn.close()
    return jsonify(row)

if __name__ == '__main__':
    app.run(port=1966, debug=True)
