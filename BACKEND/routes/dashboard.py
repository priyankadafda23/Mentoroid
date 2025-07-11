from flask import Blueprint, jsonify, request
from models import db, Course, User, Enrollment

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/student', methods=['GET'])
def student_dashboard():
    student_id = request.args.get('student_id')
    if not student_id:
        return jsonify({'error': 'Missing student ID'}), 400

    enrolled_ids = [e.course_id for e in Enrollment.query.filter_by(student_id=student_id).all()]
    
    all_courses = Course.query.all() 

    enrolled_courses_details = [c for c in all_courses if c.id in enrolled_ids]

    return jsonify({
        'enrolled': enrolled_ids,
        'my_enrolled': [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'thumbnail': c.thumbnail
        } for c in enrolled_courses_details],
        'courses': [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'thumbnail': c.thumbnail
        } for c in all_courses] # Return all_courses here
    })



@dashboard_bp.route('/dashboard/teacher', methods=['GET'])
def get_teacher_dashboard():
    teacher_id = request.args.get('id')
    if not teacher_id:
        return jsonify({'error': 'Missing teacher ID'}), 400

    courses = Course.query.filter_by(teacher_id=teacher_id).all()

    my_courses = []
    for course in courses:
        student_count = Enrollment.query.filter_by(course_id=course.id).count()
        my_courses.append({
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'students': student_count,
            'thumbnail': course.thumbnail
        })

    actions = [
        {'title': 'Upload New Course', 'link': '/courses/create'},
        {'title': 'Update Existing Course', 'link': '/courses/edit '},
        {'title': 'Upload Quiz', 'link': '/quiz/create'},
        {'title': 'Assign Marks to Quiz', 'link': '/quiz/review'},
        {'title': 'Check Leaderboard', 'link': '/quiz/leaderboard'}
    ]

    return jsonify({'my_courses': my_courses, 'actions': actions})
