import os
import json
import openai
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from transformers import pipeline

# LangChain imports
from langchain_community.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain

# Load environment variables
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

sentiment_analyzer = pipeline(task='sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

try:
    client_credentials_manager = SpotifyClientCredentials(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
except Exception as e:
    print(f"Error initializing Spotify client: {e}")
    sp = None

def get_spotify_recommendations(mood):
    if not sp:
        print("Spotify client not initialized")
        return []

    try:
        mood_queries = {
            "happy": {
                "query": "happy mood playlist",
                "genres": ["pop", "dance", "happy"]
            },
            "sad": {
                "query": "sad mood playlist",
                "genres": ["acoustic", "sad", "rainy-day"]
            },
            "neutral": {
                "query": "chill mood playlist",
                "genres": ["ambient", "chill", "relaxative"]
            }
        }

        mood_info = mood_queries.get(mood, mood_queries["neutral"])

        results = sp.search(
            q=mood_info["query"],
            type='playlist',
            limit=2,
            market='US'
        )

        if not results or 'playlists' not in results or 'items' not in results['playlists']:
            print("No playlist results found")
            return []

        playlists = []
        for playlist in results['playlists']['items']:
            if playlist and 'name' in playlist and 'external_urls' in playlist:
                playlists.append({
                    "name": playlist['name'],
                    "url": playlist['external_urls']['spotify']
                })

        return playlists

    except Exception as e:
        print(f"Error getting Spotify recommendations: {e}")
        return []

def generate_personalized_message(mood):
    prompt = f"Provide a simple joke for someone feeling {mood}. In your return response, just say \"here is a Joke:\" and then tells the joke"
    response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
            )
    return response.choices[0].message.content.strip()

def generate_support_response(text, mood):
    template = """The user has journaled the following:

{text}

The user seems to be feeling {mood}. Provide a supportive response in JSON format with two keys: 
'validation' (a short empathic message acknowledging their feelings) and 
'coping_strategies' (a JSON array of at least two actionable coping suggestions).
"""

    prompt = PromptTemplate(
        input_variables=["text", "mood"],
        template=template,
    )
    llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), model_name="gpt-3.5-turbo")

    chain = LLMChain(prompt=prompt, llm=llm)
    support_json = chain.run(text=text, mood=mood).strip()

    try:
        support_data = json.loads(support_json)
        if "validation" in support_data and "coping_strategies" in support_data:
            return support_data
    except json.JSONDecodeError:
        pass

    return {
        "validation": "I hear how challenging this is and it's understandable to feel this way.",
        "coping_strategies": [
            "Try a short mindfulness exercise, focusing on your breath for a few minutes.",
            "Write down three things you're grateful for today to shift your mindset."
        ]
    }

def analyze_sentiment(text):
    sentiment = sentiment_analyzer(text)[0]
    mood = sentiment['label']
    score = sentiment['score']

    if mood == "POSITIVE":
        mood_category = "happy"
    elif mood == "NEGATIVE":
        mood_category = "sad"
    else:
        mood_category = "neutral"

    return mood_category, score
