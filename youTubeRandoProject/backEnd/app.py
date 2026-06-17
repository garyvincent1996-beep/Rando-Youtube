from flask import Flask, request, jsonify
import sys
import os

# Add the path to the Python script
sys.path.append(r"c:\Users\garyv\OneDrive\Documents\Python Beginner Programs")

# Import the function from the script
from youTubeRandomizer import find_random_video, pretty_time

app = Flask(__name__, static_folder='.')

@app.route('/')
def home():
    return app.send_static_file('youTubeRandomizer.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    target_minutes = request.args.get('target', 10, type=int)

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    video, error = find_random_video(query, target_minutes=target_minutes)

    if error:
        return jsonify({'error': error}), 404

    return jsonify({
        'title': video['title'],
        'length': pretty_time(video['duration_seconds']),
        'url': video['url']
    })

if __name__ == '__main__':
    app.run(debug=True)