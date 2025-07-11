from flask import Blueprint, jsonify
from models import db, Quiz, QuizSubmission, QuizAnswer, User

leaderboard_bp = Blueprint('leaderboard', __name__)

# Helper function to add CORS headers
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'mentoroid-zeta.vercel.app'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@leaderboard_bp.route('/leaderboard/<int:quiz_id>', methods=['GET'])
def get_leaderboard(quiz_id):
    try:
        # Verify quiz exists
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            response = jsonify({'error': 'Quiz not found'})
            return add_cors_headers(response), 404

        # Get all submissions for this quiz with user details
        submissions = db.session.query(
            QuizSubmission.id,
            QuizSubmission.student_id,
            QuizSubmission.submitted_at,
            QuizSubmission.time_taken,
            QuizSubmission.score,
            User.name.label('student_name')
        ).join(User, User.id == QuizSubmission.student_id)\
        .filter(QuizSubmission.quiz_id == quiz_id)\
        .order_by(
            QuizSubmission.score.desc(),  # Order by score first (highest first)
            QuizSubmission.time_taken.asc()  # Then by time taken (fastest first)
        ).all()

        # Format the leaderboard data
        leaderboard = [{
            'student_name': s.student_name,
            'student_id': s.student_id,
            'submitted_at': s.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if s.submitted_at else None,
            'time_taken': s.time_taken,
            'score': s.score
        } for s in submissions]

        response = jsonify(leaderboard)
        return add_cors_headers(response)

    except Exception as e:
        print(f"Error fetching leaderboard: {str(e)}")
        response = jsonify({'error': 'Server error fetching leaderboard'})
        return add_cors_headers(response), 500

# Add CORS headers to all responses
@leaderboard_bp.after_request
def after_request(response):
    return add_cors_headers(response)

# Optional: Get detailed submission info for a specific student
@leaderboard_bp.route('/leaderboard/<int:quiz_id>/student/<int:student_id>', methods=['GET'])
def get_student_submission_details(quiz_id, student_id):
    try:
        # Get the submission
        submission = QuizSubmission.query.filter_by(
            quiz_id=quiz_id, 
            student_id=student_id
        ).first()
        
        if not submission:
            response = jsonify({'error': 'Submission not found'})
            return add_cors_headers(response), 404

        # Get all answers for this submission
        answers = db.session.query(
            QuizAnswer.question_id,
            QuizAnswer.answer,
            QuizAnswer.is_correct,
            Question.text.label('question_text'),
            Question.type.label('question_type'),
            Question.options,
            Question.correct_option
        ).join(Question, Question.id == QuizAnswer.question_id)\
         .filter(QuizAnswer.submission_id == submission.id)\
         .all()

        # Format the response
        submission_details = {
            'submission_id': submission.id,
            'score': submission.score,
            'time_taken': submission.time_taken,
            'submitted_at': submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
            'answers': [{
                'question_id': a.question_id,
                'question_text': a.question_text,
                'question_type': a.question_type,
                'options': a.options,
                'correct_option': a.correct_option,
                'student_answer': a.answer,
                'is_correct': a.is_correct
            } for a in answers]
        }

        response = jsonify(submission_details)
        return add_cors_headers(response)

    except Exception as e:
        print(f"Error fetching submission details: {str(e)}")
        response = jsonify({'error': 'Server error fetching submission details'})
        return add_cors_headers(response), 500


@leaderboard_bp.route('/quizzes', methods=['GET'])
def get_quizzes():
    try:
        # Fetch all quizzes from database
        quizzes = Quiz.query.all()
        
        # Convert to list of dictionaries
        quiz_list = []
        for quiz in quizzes:
            quiz_data = {
                'id': quiz.id,
                'title': quiz.title,
                'instructions': quiz.instructions if hasattr(quiz, 'instructions') else '',
                'created_at': quiz.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(quiz, 'created_at') and quiz.created_at else 'No date'
            }
            quiz_list.append(quiz_data)
        
        return jsonify(quiz_list)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch quizzes'}), 500