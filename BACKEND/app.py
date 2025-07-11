from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.auth import auth_bp
from routes.courses import course_bp
from models import db
from routes.dashboard import dashboard_bp
from routes.notifications import notif_bp
from routes.youtube import youtube_bp
from routes.quiz import quiz_bp
from leaderboard import leaderboard_bp

import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


CORS(app, 
     origins=["https://mentoroid-zeta.vercel.app"],
     supports_credentials=True)



app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")


db.init_app(app)

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(course_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(notif_bp)
app.register_blueprint(youtube_bp)
app.register_blueprint(leaderboard_bp)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'Flask backend is working!'


if __name__ == '__main__':
    app.run(debug=True)