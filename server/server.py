from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
import os
from gtts import gTTS
import time
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

def ai_generate_response(user_input):
    GOOGLE_API_KEY = "AIzaSyDO3yKGP_m1bhXwBFJVeJrgdDmVigVDu98"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    initial_prompt = (
        "THE PROMPT MUST BE RELATED TO THERAPY!!!, YOU CAN ONLY ANSWER ABOUT THERAPY!! IF A PROMPT IS NOT RELATED TO THERAPY, OR ANY SERVICES YOU CAN PROVIDE, JUST SAY THAT AS A THERAPIST, YOU CANNOT ANSWER THAT, YOU ARE A THERAPIST, GIVE ANSWERS ABOUT ISSUES"
        "You are a highly experienced psychotherapist with many years of experience. "
        "You are here to provide emotional support and guidance. Your responses should be "
        "empathetic, validating, and comforting. Always respond as if you are speaking to a client in a therapy session."
    )
    try:
        prompt = f"{initial_prompt}\nClient: {user_input}\nTherapist:"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"


def save_audio():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        filename = os.path.join('server/static/audio', 'recorded_audio.wav')
        audio_file.save(filename)
        audio_file_url = f'/static/audio/recorded_audio.wav' 
        return jsonify({'audio_file_url': audio_file_url})
    else:
        return jsonify({'error': 'No audio file provided'})


def generate_response(user_input):    
    response = ai_generate_response(user_input)
    if user_input.lower() != " ":
        return response
    else:
        return "I'm sorry, I didn't understand that."

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    timestamp = str(int(time.time()))
    audio_file = os.path.join('static/audio', f'output_{timestamp}.mp3')
    tts.save(audio_file)
    return audio_file

@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    if 'text' in data:
        user_message = data['text']
        bot_response = generate_response(user_message)
        if bot_response:
            audio_file_path = text_to_speech(bot_response)
            audio_file_url = url_for('serve_audio', filename=os.path.basename(audio_file_path), _external=True)
            return jsonify({'text': bot_response, 'audio_file_url': audio_file_url})
        else:
            return jsonify({'error': 'Failed to generate bot response'})
    else:
        return jsonify({'error': 'No text provided'})

if __name__ == '__main__':
    os.makedirs('static/audio', exist_ok=True)
    app.run()
