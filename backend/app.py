import os
from flask import Flask, request, jsonify
from transformers import pipeline
import openai
from flask_cors import CORS
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Hugging Face sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Initialize Spotify API client
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running."})

@app.route('/analyze', methods=['POST'])
def analyze_mood():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Sentiment Analysis using Hugging Face
    sentiment = sentiment_analyzer(text)[0]
    mood = sentiment['label']
    score = sentiment['score']

    # Map sentiment to mood categories
    if mood == "POSITIVE":
        mood_category = "happy"
    elif mood == "NEGATIVE":
        mood_category = "sad"
    else:
        mood_category = "neutral"

    # Generate personalized music recommendations
    music_recommendations = get_spotify_recommendations(mood_category)

    # Generate a personalized message using OpenAI
    personalized_message = generate_personalized_message(mood_category)

    return jsonify({
        "mood": mood_category,
        "music_recommendations": music_recommendations,
        "personalized_message": personalized_message
    })

def get_spotify_recommendations(mood):
    # Define mood-based search queries
    mood_queries = {
        "happy": "happy",
        "sad": "sad",
        "neutral": "ambient"
    }

    query = mood_queries.get(mood, "ambient")

    # Search for playlists related to the mood
    results = sp.search(q=query, type='playlist', limit=2)

    playlists = []
    for playlist in results['playlists']['items']:
        playlists.append({
            "name": playlist['name'],
            "url": playlist['external_urls']['spotify']
        })

    return playlists

def generate_personalized_message(mood):
    prompt = f"Provide a supportive message for someone feeling {mood}."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].text.strip()
    return message

if __name__ == '__main__':
    app.run(debug=True)
