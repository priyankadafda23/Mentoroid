from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(200), nullable=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    level = db.Column(db.String(20))
    description = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(500), nullable=True)
    youtube_link = db.Column(db.String(300), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    students = db.Column(db.Integer, default=0)

    teacher = db.relationship('User', backref='courses')


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')
    students = db.Column(db.Integer, default=0)

    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    
    recipient = db.relationship('User', backref='notifications')

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    instructions = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', cascade="all, delete-orphan")
    submissions = db.relationship('QuizSubmission', backref='quiz', cascade="all, delete-orphan")
    teacher = db.relationship('User', backref='created_quizzes')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # short, long, mcq, number
    options = db.Column(db.JSON, nullable=True)  # Only used for MCQ
    correct_option = db.Column(db.Integer, nullable=True)  # For MCQ questions
    
    # Relationships
    student_answers = db.relationship('QuizAnswer', backref='question', cascade="all, delete-orphan")

class QuizSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)  # Time in seconds
    score = db.Column(db.Float, nullable=True)  # Score achieved (percentage)
    submitted_at = db.Column(db.DateTime, default=datetime.now())
    
    # Relationships
    student = db.relationship('User', backref='quiz_submissions')
    answers = db.relationship('QuizAnswer', backref='submission', cascade="all, delete-orphan")
    
    __table_args__ = (db.UniqueConstraint('quiz_id', 'student_id', name='unique_quiz_student'),)

class QuizAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('quiz_submission.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)  # Student's answer
    is_correct = db.Column(db.Boolean, default=False)  # Whether answer is correct
    
    __table_args__ = (db.UniqueConstraint('submission_id', 'question_id', name='unique_submission_question'),)