from flask import Flask, request, jsonify
from flask_cors import CORS 
import sys
import os

# File to the Python script
sys.path.append(r"c:\Users\garyv\OneDrive\Documents\Projects\YouTubeRandomizer\backEnd")

# Imports the functions from the script
from youTubeRandomizer import find_random_video, pretty_time

app = Flask(__name__, static_folder='.')
CORS(app) # <-- Allows frontend to talk to this API

@app.route('/')
def home():
    # Note: Since you are using http.server for the frontend now,
    # you might not even need this route, but it doesn't hurt.
    return "Backend is running!"

@app.route('/search', methods=['GET'])
def search():
    # Matches frontend's request for query (q) and target time
    query = request.args.get('q', '')
    target_minutes = request.args.get('target', 10, type=int)

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Calls the logic from youTubeRandomizer.py
    video, error = find_random_video(query, target_minutes=target_minutes)

    if error:
        return jsonify({'error': error}), 404

    #'jsonify' sends the video data back to JavaScript fetch()
    return jsonify({
        'title': video['title'],
        'length': pretty_time(video['duration_seconds']),
        'url': video['url']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)