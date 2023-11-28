from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    num_questions = db.Column(db.Integer, nullable=False)
    quiz_date = db.Column(db.Date, nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        if username == 'admin' and password == hashlib.sha256('password'.encode()).hexdigest():
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    students = Student.query.all()
    quizzes = Quiz.query.all()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/<int:student_id>')
def student_results(student_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    student = Student.query.get(student_id)
    results = db.session.query(Result, Quiz).join(Quiz).filter(Result.student_id == student_id).all()
    return render_template('student_results.html', student=student, results=results)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        new_student = Student(first_name=first_name, last_name=last_name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = datetime.strptime(request.form['quiz_date'], '%Y-%m-%d')
        new_quiz = Quiz(subject=subject, num_questions=num_questions, quiz_date=quiz_date)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_quiz.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        new_result = Result(student_id=student_id, quiz_id=quiz_id, score=score)
        db.session.add(new_result)
        db.session.commit()
        return redirect(url_for('dashboard'))
    students = Student.query.all()
    quizzes = Quiz.query.all()
    return render_template('results.html', students=students, quizzes=quizzes)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully.')
    else:
        flash('Student not found.')
    return redirect(url_for('dashboard'))

@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully.')
    else:
        flash('Quiz not found.')
    return redirect(url_for('dashboard'))

def initialize_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
