from flask import Blueprint, request, jsonify
from ai_models import (
    analyze_sentiment,
    get_spotify_recommendations,
    generate_personalized_message,
    generate_support_response
)

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running."})

@bp.route('/analyze', methods=['POST'])
def analyze_mood():
    try:
        data = request.json
        title = data.get("title", "")
        location = data.get("location", "")
        weather = data.get("weather", "")
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        mood_category, _ = analyze_sentiment(text)
        music_recommendations = get_spotify_recommendations(mood_category)
        personalized_message = None
        if mood_category == 'sad':
            try:
                personalized_message = generate_personalized_message(mood_category)
                # print(f'look at here---------------------{personalized_message}')
            except Exception as e:
                print(f"Error generating message: {e}")
                personalized_message = "Thank you for sharing your feelings!"

        try:
            support_response = generate_support_response(text, mood_category)
        except Exception as e:
            print(f"Error generating support response: {e}")
            support_response = {
                "validation": "I understand it might be tough.",
                "coping_strategies": ["Take a short walk.", "Try deep breathing."]
            }
            
        return jsonify({
            "mood": mood_category,
            "music_recommendations": music_recommendations,
            "personalized_message": personalized_message,
            "support_response": support_response if support_response else ''
        })

    except Exception as e:
        print(f"Error in analyze_mood: {e}")
        return jsonify({"error": "An error occurred processing your request"}), 500
