import requests
from flask import Blueprint, jsonify
from models import Course
from routes.youtube import YOUTUBE_API_KEY
from dotenv import load_dotenv
import os

load_dotenv()

api_url = os.getenv("YOUTUBE_API_URL")

course_detail_bp = Blueprint('course_detail', __name__)

@course_detail_bp.route('/youtube-videos/<int:course_id>', methods=['GET'])
def get_youtube_videos(course_id):
    course = Course.query.get(course_id)
    if not course or not course.youtube_link:
        return jsonify({'videos': []})

    url = course.youtube_link.strip()
    videos = []

    try:
        if "list=" in url:
            playlist_id = url.split("list=")[1].split("&")[0]
            api_url = f"{api_url}/playlistItems?part=snippet&maxResults=20&playlistId={playlist_id}&key={YOUTUBE_API_KEY}"
            res = requests.get(api_url)
            items = res.json().get('items', [])
            videos = [{
                'title': item['snippet']['title'],
                'videoId': item['snippet']['resourceId']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            } for item in items]

        elif "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
            api_url = f"{api_url}/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
            res = requests.get(api_url)
            items = res.json().get('items', [])
            if items:
                item = items[0]
                videos = [{
                    'title': item['snippet']['title'],
                    'videoId': video_id,
                    'thumbnail': item['snippet']['thumbnails']['medium']['url']
                }]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            api_url = f"{api_url}/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
            res = requests.get(api_url)
            items = res.json().get('items', [])
            if items:
                item = items[0]
                videos = [{
                    'title': item['snippet']['title'],
                    'videoId': video_id,
                    'thumbnail': item['snippet']['thumbnails']['medium']['url']
                }]
        return jsonify({'videos': videos})
    
    except Exception as e:
        print("Error fetching video:", e)
        return jsonify({'videos': []})
