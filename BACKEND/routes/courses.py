from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment, Notification
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

course_bp = Blueprint('course', __name__)
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("cloud_name"),
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("api_secret")
)


@course_bp.route('/create-course', methods=['POST'])
def create_course():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        teacher_id = request.form.get('teacher_id')
        youtube_link = request.form.get('youtube_link')
        thumbnail_file = request.files.get('thumbnail')

        print("Received data:")
        print("Title:", title)
        print("Description:", description)
        print("Teacher ID:", teacher_id)
        print("YouTube Link:", youtube_link)
        print("Thumbnail:", thumbnail_file)

        if not all([title, description, teacher_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        thumbnail_url = None
        if thumbnail_file:
            upload_result = cloudinary.uploader.upload(thumbnail_file)
            thumbnail_url = upload_result['secure_url']

        new_course = Course(
            title=title,
            description=description,
            thumbnail=thumbnail_url,
            teacher_id=teacher_id,
            youtube_link=youtube_link
        )
        db.session.add(new_course)

        # Notify all students
        students = User.query.filter_by(role='student').all()
        for student in students:
            notif = Notification(
                recipient_id=student.id,
                message=f'New course uploaded: {title}',
                is_read=False
            )
            db.session.add(notif)
        
        db.session.commit()
        return jsonify({'message': 'Course created successfully'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to create course: {str(e)}'}), 500


@course_bp.route('/enroll/<int:course_id>', methods=['POST'])
def enroll_in_course(course_id):
    data = request.get_json()
    student_id = data.get('student_id')

    if not student_id:
        return jsonify({'error': 'Missing student ID'}), 400

    # Prevent duplicate
    if Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first():
        return jsonify({'error': 'Already enrolled'}), 400

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)

    # Increment student count
    course = Course.query.get(course_id)
    if course.students is None:
        course.students = 1
    else:
        course.students += 1

    # Notify teacher
    notification = Notification(
        recipient_id=course.teacher_id,
        message=f"A student has enrolled in your course: {course.title}"
    )
    db.session.add(notification)

    db.session.commit()

    return jsonify({'message': 'Enrolled successfully'})


@course_bp.route('/course/<int:id>')
def get_course_by_id(id):
    course = Course.query.get(id)
    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'youtube_link': course.youtube_link
    })


@course_bp.route('/course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    student_id = request.args.get('student_id')

    if student_id and Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first():
        enrolled = True
    else:
        enrolled = False

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'youtube_link': course.youtube_link,
        'teacher_id': int(course.teacher_id),
        'enrolled': enrolled,
        'thumbnail': course.thumbnail
    })


@course_bp.route('/update-course/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        teacher_id = request.form.get('teacher_id')
        if not teacher_id:
            return jsonify({'error': 'Missing teacher ID'}), 400

        # Ensure teacher_id is an integer
        try:
            teacher_id = int(teacher_id)
        except ValueError:
            return jsonify({'error': 'Invalid teacher ID'}), 400
        
        # Simple authorization check - just ensure the course belongs to the teacher
        course = Course.query.filter_by(id=course_id, teacher_id=teacher_id).first()
        if not course:
            return jsonify({'error': 'You are not authorized to edit this course.'}), 403

        # Get update fields
        title = request.form.get('title')
        description = request.form.get('description')
        youtube_link = request.form.get('youtube_link')
        thumbnail_file = request.files.get('thumbnail')

        if title:
            course.title = title
        if description:
            course.description = description
        if youtube_link:
            course.youtube_link = youtube_link
        if thumbnail_file:
            upload_result = cloudinary.uploader.upload(thumbnail_file)
            course.thumbnail = upload_result['secure_url']

        db.session.commit()
        return jsonify({'message': 'Course updated successfully'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to update course: {str(e)}'}), 500

