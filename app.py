import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "STUDENT.db"

def get_db_connection():
    conn = sqlite3.connect('STUDENT.db')  
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS RECORD (
        ROLL_NO INT NOT NULL,
        ADM_NO INT PRIMARY KEY,
        NAME VARCHAR(35) NOT NULL,
        CLASS VARCHAR(5) NOT NULL,
        ENGLISH INT CHECK (ENGLISH BETWEEN 0 AND 100),
        GR1 VARCHAR(2),
        HINDI INT CHECK (HINDI BETWEEN 0 AND 100),
        GR2 VARCHAR(2),
        MATHEMATICS INT CHECK (MATHEMATICS BETWEEN 0 AND 100),
        GR3 VARCHAR(2),
        SCIENCE INT CHECK (SCIENCE BETWEEN 0 AND 100),
        GR4 VARCHAR(2),
        SOCIAL_SCIENCE INT CHECK (SOCIAL_SCIENCE BETWEEN 0 AND 100),
        GR5 VARCHAR(2),
        TOTAL INT,
        PERCENTAGE FLOAT (5,2),
        RESULT CHAR(4)
    );
    """)
    conn.commit()
    conn.close()

init_db()

def calculate_grade(marks):
    if marks>=91 and marks<=100: return "A1" 
    elif marks>=81 and marks<=90: return "A2" 
    elif marks>=71 and marks<=80: return "B1" 
    elif marks>=61 and marks<=70: return "B2" 
    elif marks>=51 and marks<=60: return "C1" 
    elif marks>=41 and marks<=50: return "C2" 
    elif marks>=33 and marks<=40: return "D" 
    else: return "E"
    
@app.route("/")
def dashboard():
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("SELECT * FROM RECORD ORDER BY ROLL_NO")
    students = cur.fetchall()
    cur.execute("""SELECT AVG(ENGLISH) as avg_eng, MAX(ENGLISH) as max_eng, MIN(ENGLISH) as min_eng, AVG(HINDI) as avg_hin, MAX(HINDI) as max_hin, MIN(HINDI) as min_hin, AVG(MATHEMATICS) as avg_mat, MAX(MATHEMATICS) as max_mat, MIN(MATHEMATICS) as min_mat, AVG(SCIENCE) as avg_sci, MAX(SCIENCE) as max_sci, MIN(SCIENCE) as min_sci, AVG(SOCIAL_SCIENCE) as avg_soc, MAX(SOCIAL_SCIENCE) as max_soc, MIN(SOCIAL_SCIENCE) as min_soc FROM RECORD""")
    analysis = cur.fetchone()
    cur.execute("SELECT NAME, PERCENTAGE FROM RECORD ORDER BY PERCENTAGE DESC")
    merit_list = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', students=students, analysis=analysis, merit_list=merit_list)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method=="POST":
        roll_no = int(request.form["roll_no"])
        adm_no = int(request.form['adm_no'])
        name = request.form['name']
        student_class = request.form['student_class']
        eng = int(request.form['english'])
        hin = int(request.form['hindi'])
        mat = int(request.form['mathematics'])
        sci = int(request.form['science'])
        soc = int(request.form['social_science'])
        gr1 = calculate_grade(eng)
        gr2 = calculate_grade(hin)
        gr3 = calculate_grade(mat)
        gr4 = calculate_grade(sci)
        gr5 = calculate_grade(soc)
        total_marks = eng + hin + mat + sci + soc
        percentage = (total_marks / 500) * 100
        if "E" in [gr1, gr2, gr3, gr4, gr5] or percentage < 33:
            result_status = "FAIL"
        else:
            result_status = "PASS"
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO RECORD (
                ROLL_NO, ADM_NO, NAME, CLASS, 
                ENGLISH, GR1, HINDI, GR2, MATHEMATICS, GR3, 
                SCIENCE, GR4, SOCIAL_SCIENCE, GR5, 
                TOTAL, PERCENTAGE, RESULT
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            roll_no, adm_no, name, student_class,
            eng, gr1, hin, gr2, mat, gr3,
            sci, gr4, soc, gr5,
            total_marks, round(percentage, 2), result_status
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/update/<int:adm_no>', methods = ['GET', 'POST'])
def update_student(adm_no):
    conn=get_db_connection()
    cur=conn.cursor()
    if request.method == 'POST':
        eng = int(request.form['english'])
        hin = int(request.form['hindi'])
        mat = int(request.form['mathematics'])
        sci = int(request.form['science'])
        soc = int(request.form['social_science'])
        gr1 = calculate_grade(eng)
        gr2 = calculate_grade(hin)
        gr3 = calculate_grade(mat)
        gr4 = calculate_grade(sci)
        gr5 = calculate_grade(soc)
        total_marks = eng + hin + mat + sci + soc
        percentage = (total_marks / 500) * 100
        if "E" in [gr1, gr2, gr3, gr4, gr5] or percentage < 33:
            result_status = "FAIL"
        else:
            result_status = "PASS"
        cur.execute("""UPDATE RECORD SET ENGLISH=?, GR1=?, HINDI=?, GR2=?, MATHEMATICS=?, GR3=?, SCIENCE=?, GR4=?, SOCIAL_SCIENCE=?, GR5=?, TOTAL=?, PERCENTAGE=?, RESULT=? WHERE ADM_NO=?""", (eng, gr1, hin, gr2, mat, gr3, sci, gr4, soc, gr5, total_marks, round(percentage, 2), result_status, adm_no))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    cur.execute("SELECT * FROM RECORD WHERE ADM_NO = ?",(adm_no))
    student = cur.fetchone()
    conn.close()
    return render_template('update_student.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)