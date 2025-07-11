from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

youtube_bp = Blueprint('youtube', __name__)
load_dotenv()

apikey = os.getenv("YOUTUBE_API_KEY")

@youtube_bp.route('/fetch-playlist', methods=['GET'])
def fetch_playlist():
    playlist_url = request.args.get('url')
    if not playlist_url:
        return jsonify({'error': 'Missing URL'}), 400

    # Extract playlist ID from URL
    if "list=" in playlist_url:
        playlist_id = playlist_url.split("list=")[1].split("&")[0]
    else:
        return jsonify({'error': 'Invalid playlist URL'}), 400

    videos = []
    next_page_token = ''

    while True:
        api_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=10&playlistId={playlist_id}&key={apikey}&pageToken={next_page_token}"
        res = requests.get(api_url).json()

        for item in res.get('items', []):
            snippet = item['snippet']
            videos.append({
                'title': snippet['title'],
                'videoId': snippet['resourceId']['videoId'],
                'thumbnail': snippet['thumbnails']['medium']['url']
            })

        next_page_token = res.get('nextPageToken')
        if not next_page_token:
            break

    return jsonify(videos)


@youtube_bp.route('/fetch-video-details', methods=['GET'])
def fetch_video_details():
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'Missing video ID'}), 400

    try:
        api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={apikey}"
        res = requests.get(api_url).json()

        if 'error' in res:
            return jsonify({'error': res['error']['message']}), res['error']['code']

        if res and res.get('items'):
            video_item = res['items'][0]
            snippet = video_item['snippet']
            
            video_data = {
                'videoId': video_id,
                'title': snippet.get('title', 'No Title'),
                'description': snippet.get('description', 'No Description'),
                'thumbnail': snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else snippet['thumbnails']['default']['url']
            }
            return jsonify(video_data)
        else:
            return jsonify({'error': 'Video not found or no items in response'}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network or API request error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

