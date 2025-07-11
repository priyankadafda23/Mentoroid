from flask import Blueprint, request, jsonify
from models import db, Quiz, Question, Notification, User, Enrollment, QuizSubmission, QuizAnswer
from datetime import datetime
import traceback
from flask_cors import cross_origin
from dotenv import load_dotenv
import os

quiz_bp = Blueprint('quiz', __name__)
load_dotenv()

cors_origin = os.getenv("CORS_ORIGINS")

# Helper function to add CORS headers
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# ✅ Create Quiz + Add Questions + Send Notifications
@quiz_bp.route('/quiz/create', methods=['POST', 'OPTIONS'])
def create_quiz():
    try:
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'OK'})
            return add_cors_headers(response), 200

        data = request.get_json()
        instructions = data.get('instructions')
        teacher_id = data.get('teacher_id')
        course_id = data.get('course_id')
        questions_data = data.get('questions')
        title = data.get('title', 'course_id')  # Add title support

        if not instructions:
            return jsonify({'error': 'Missing instruction'}), 400
        elif not teacher_id:
            return jsonify({'error': 'Missing teacher'}), 400
        elif not course_id:
            return jsonify({'error': 'Missing course_id'}), 400
        elif not questions_data:
            return jsonify({'error': 'Missing questions'}), 400

        new_quiz = Quiz(
            title=title,
            instructions=instructions,
            teacher_id=teacher_id,
            course_id=course_id
        )
        db.session.add(new_quiz)
        db.session.flush()  # Get new_quiz.id before commit

        for q in questions_data:
            if not q.get('text') or not q.get('type'):
                continue

            new_q = Question(
                quiz_id=new_quiz.id,
                text=q['text'],
                type=q['type'],
                options=q.get('options'),
                correct_option=q.get('correct_option')
            )
            db.session.add(new_q)

        # Notify all enrolled students in the course
        enrolled_students = Enrollment.query.filter_by(course_id=course_id).all()
        for enrollment in enrolled_students:
            notif = Notification(
                recipient_id=enrollment.student_id,
                message=f"New quiz uploaded in your course (ID: {course_id})",
                is_read=False
            )
            db.session.add(notif)

        db.session.commit()
        response = jsonify({'message': 'Quiz created successfully with notifications'})
        return add_cors_headers(response), 200

    except Exception as e:
        traceback.print_exc()
        response = jsonify({'error': f'Server error: {str(e)}'})
        return add_cors_headers(response), 500

# ✅ Get all quizzes for a student (mapped to their enrolled courses)
@quiz_bp.route('/quiz/student', methods=['GET'])
def get_quizzes_for_student():
    student_id = request.args.get('student_id')
    if not student_id:
        response = jsonify({'error': 'Missing student ID'})
        return add_cors_headers(response), 400

    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    course_ids = [e.course_id for e in enrollments]

    quizzes = Quiz.query.filter(Quiz.course_id.in_(course_ids)).all()

    course_quiz_map = {}
    for quiz in quizzes:
        if quiz.course_id not in course_quiz_map:
            course_quiz_map[quiz.course_id] = []

        course_quiz_map[quiz.course_id].append({
            'id': quiz.id,
            'title': quiz.title,
            'instructions': quiz.instructions,
        })

    response = jsonify(course_quiz_map)
    return add_cors_headers(response)

# ✅ Get quiz detail + questions
@quiz_bp.route("/quiz/<int:quiz_id>", methods=['GET'])
def get_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        response = jsonify({"error": "Quiz not found"})
        return add_cors_headers(response), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    response = jsonify({
        "id": quiz.id,
        "title": quiz.title,
        "instructions": quiz.instructions,
        "questions": [
            {
                "id": q.id,
                "text": q.text,
                "type": q.type,
                "options": q.options
            } for q in questions
        ]
    })
    return add_cors_headers(response)

# ✅ Submit Quiz with Score Calculation
@quiz_bp.route("/submit-quiz/<int:quiz_id>", methods=["POST", "OPTIONS"])
def submit_quiz(quiz_id):
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        return add_cors_headers(response), 200
    
    try:
        data = request.get_json()
        student_id = data["student_id"]
        answers = data["answers"]  # List of {question_id, answer}
        time_taken = data["time_taken"]

        # Check if student already submitted this quiz
        existing_submission = QuizSubmission.query.filter_by(
            quiz_id=quiz_id, 
            student_id=student_id
        ).first()
        
        if existing_submission:
            response = jsonify({"error": "You have already submitted this quiz"})
            return add_cors_headers(response), 400

        # Calculate score
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        total_questions = len(questions)
        correct_answers = 0
        
        # Create submission record
        submission = QuizSubmission(
            quiz_id=quiz_id,
            student_id=student_id,
            time_taken=time_taken
        )
        db.session.add(submission)
        db.session.flush()  # Get submission ID

        # Process each answer
        for answer_data in answers:
            question_id = answer_data["question_id"]
            student_answer = answer_data["answer"]
            
            # Find the question
            question = Question.query.get(question_id)
            if not question:
                continue
                
            is_correct = False
            
            # Check if answer is correct based on question type
            if question.type == 'mcq':
                if question.correct_option is not None:
                    is_correct = student_answer == question.correct_option
            # For other question types, you might want to implement different logic
            # or manual grading system
            
            if is_correct:
                correct_answers += 1
            
            # Store individual answer
            quiz_answer = QuizAnswer(
                submission_id=submission.id,
                question_id=question_id,
                answer=student_answer,
                is_correct=is_correct
            )
            db.session.add(quiz_answer)

        # Calculate final score (percentage)
        if total_questions > 0:
            score = (correct_answers / total_questions) * 100
        else:
            score = 0
            
        submission.score = score
        db.session.commit()
        
        response = jsonify({
            "message": "Quiz submitted successfully", 
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions
        })
        return add_cors_headers(response)
        
    except Exception as e:
        traceback.print_exc()
        response = jsonify({"error": str(e)})
        return add_cors_headers(response), 500

# ✅ Leaderboard (Updated to use correct tables)
@quiz_bp.route("/leaderboard/<int:quiz_id>", methods=['GET'])
def leaderboard(quiz_id):
    try:
        # Verify quiz exists
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            response = jsonify({'error': 'Quiz not found'})
            return add_cors_headers(response), 404

        # Get submissions with user details from QuizSubmission table
        submissions = db.session.query(
            QuizSubmission.id,
            QuizSubmission.student_id,
            QuizSubmission.submitted_at,
            QuizSubmission.time_taken,
            QuizSubmission.score,  # This is the correct score from QuizSubmission
            User.name.label('student_name')
        ).join(User, User.id == QuizSubmission.student_id)\
         .filter(QuizSubmission.quiz_id == quiz_id)\
         .order_by(
             QuizSubmission.score.desc(),  # Order by score first (highest first)
             QuizSubmission.time_taken.asc()  # Then by time taken (fastest first)
         ).all()

        result = []
        for sub in submissions:
            result.append({
                "student_id": sub.student_id,
                "student_name": sub.student_name,
                "time_taken": sub.time_taken,
                "score": sub.score,  # Now correctly getting score from QuizSubmission
                "submitted_at": sub.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if sub.submitted_at else None
            })

        response = jsonify(result)
        return add_cors_headers(response)

    except Exception as e:
        print(f"Error fetching leaderboard: {str(e)}")
        traceback.print_exc()
        response = jsonify({'error': 'Server error fetching leaderboard'})
        return add_cors_headers(response), 500

# ✅ Get teacher's quizzes
@quiz_bp.route('/quiz/teacher/<int:teacher_id>', methods=['GET'])
def get_teacher_quizzes(teacher_id):
    try:
        # Verify teacher exists
        teacher = User.query.filter_by(id=teacher_id, role='teacher').first()
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404

        # Get quizzes with question counts
        quizzes = db.session.query(
            Quiz.id,
            Quiz.title,
            Quiz.instructions,
            db.func.count(Question.id).label('question_count'),
            Quiz.created_at
        ).outerjoin(Question, Question.quiz_id == Quiz.id)\
         .filter(Quiz.teacher_id == teacher_id)\
         .group_by(Quiz.id)\
         .all()

        result = [{
            'id': q.id,
            'title': q.title or 'Untitled Quiz',
            'instructions': q.instructions,
            'questions': q.question_count,
            'created_at': q.created_at.strftime('%Y-%m-%d %H:%M:%S') if q.created_at else None
        } for q in quizzes]

        return add_cors_headers(jsonify(result))

    except Exception as e:
        print(f"Error fetching teacher quizzes: {str(e)}")
        return add_cors_headers(jsonify({'error': 'Server error fetching quizzes'})), 500

# Add CORS headers to all responses
@quiz_bp.after_request
def after_request(response):
    return add_cors_headers(response)

@quiz_bp.route('/quizzes', methods=['GET'])
@cross_origin(origins=[cors_origin])
def get_all_quizzes():
    try:
        quizzes = Quiz.query.all()
        quiz_list = []

        for q in quizzes:
            # Count questions properly
            question_count = 0
            if hasattr(q, 'questions') and q.questions:
                question_count = len(q.questions)
            
            quiz_list.append({
                'id': q.id,
                'title': q.title,
                'instructions': q.instructions,
                'created_at': q.created_at.strftime('%Y-%m-%d %H:%M:%S') if q.created_at else None,
                'question_count': question_count
            })

        return jsonify(quiz_list), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error fetching quizzes: {str(e)}")
        return jsonify({'error': 'Server error fetching quizzes'}), 500


@quiz_bp.route('/quizzes', methods=['OPTIONS'])
@cross_origin(origins=[cors_origin])
def handle_quizzes_options():
    return jsonify({'status': 'ok'}), 200


# Get all quiz submissions for teacher review
@quiz_bp.route('/quiz/<int:quiz_id>/submissions', methods=['GET'])
def get_quiz_submissions(quiz_id):
    submissions = QuizSubmission.query.filter_by(quiz_id=quiz_id).all()
    data = []
    for sub in submissions:
        data.append({
            'student_id': sub.student_id,
            'student_name': sub.student.name,
            'submitted_at': sub.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
            'time_taken': sub.time_taken,
            'score': sub.score
        })
    return jsonify(data)

# Update score manually and notify student
@quiz_bp.route('/quiz/<int:quiz_id>/score/<int:student_id>', methods=['POST'])
def update_quiz_score(quiz_id, student_id):
    data = request.get_json()
    new_score = data.get('score')
    feedback = data.get('feedback', '')

    sub = QuizSubmission.query.filter_by(quiz_id=quiz_id, student_id=student_id).first()
    if not sub:
        return jsonify({'error': 'Submission not found'}), 404

    sub.score = new_score
    db.session.commit()

    # Notify student
    notif = Notification(
        recipient_id=student_id,
        message=f"Your quiz score was updated to {new_score}%. Feedback: {feedback}",
        is_read=False
    )
    db.session.add(notif)
    db.session.commit()

    return jsonify({'message': 'Score updated and student notified'})


@quiz_bp.route('/quiz/<int:quiz_id>/submission/<int:student_id>', methods=['GET'])
def get_submission_detail(quiz_id, student_id):
    submission = QuizSubmission.query.filter_by(quiz_id=quiz_id, student_id=student_id).first()
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404

    answers = QuizAnswer.query.filter_by(submission_id=submission.id).all()
    question_ids = [a.question_id for a in answers]
    questions = Question.query.filter(Question.id.in_(question_ids)).all()
    question_map = {q.id: q for q in questions}

    return jsonify({
        'student_name': submission.student.name,
        'time_taken': submission.time_taken,
        'submitted_at': submission.submitted_at.strftime('%Y-%m-%d %H:%M'),
        'score': submission.score,
        'answers': [
            {
                'question': question_map[a.question_id].text,
                'type': question_map[a.question_id].type,
                'options': question_map[a.question_id].options,
                'student_answer': a.answer,
                'correct_answer': question_map[a.question_id].correct_option
            }
            for a in answers
        ]
    })


@quiz_bp.route('/student/<int:student_id>/submissions', methods=['GET'])
def get_student_submissions(student_id):
    submissions = QuizSubmission.query.filter_by(student_id=student_id).all()
    result = []
    for sub in submissions:
        quiz = Quiz.query.get(sub.quiz_id)
        result.append({
            'quiz_id': sub.quiz_id,
            'title': quiz.title if quiz else 'Untitled',
            'submitted_at': sub.submitted_at.strftime('%Y-%m-%d %H:%M'),
            'time_taken': sub.time_taken,
            'score': sub.score
        })
    return jsonify(result)


@quiz_bp.route('/student/<int:student_id>/submission/<int:quiz_id>', methods=['GET'])
def get_student_submission_detail(student_id, quiz_id):
    submission = QuizSubmission.query.filter_by(student_id=student_id, quiz_id=quiz_id).first()
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404

    answers = QuizAnswer.query.filter_by(submission_id=submission.id).all()
    question_ids = [a.question_id for a in answers]
    questions = Question.query.filter(Question.id.in_(question_ids)).all()
    question_map = {q.id: q for q in questions}

    return jsonify({
        'submitted_at': submission.submitted_at.strftime('%Y-%m-%d %H:%M'),
        'time_taken': submission.time_taken,
        'score': submission.score,
        'reviewed': submission.score is not None,
        'answers': [
            {
                'question': question_map[a.question_id].text,
                'type': question_map[a.question_id].type,
                'options': question_map[a.question_id].options,
                'student_answer': a.answer,
                'correct_answer': question_map[a.question_id].correct_option
            } for a in answers
        ]
    })
