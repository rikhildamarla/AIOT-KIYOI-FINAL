import google.generativeai as genai
from gtts import gTTS
import playsound
import os
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

GOOGLE_API_KEY = "AIzaSyDO3yKGP_m1bhXwBFJVeJrgdDmVigVDu98"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

initial_prompt = (
    "You are a highly experienced psychotherapist with many years of experience. "
    "You are here to provide emotional support and guidance. Your responses should be "
    "empathetic, validating, and comforting. Always respond as if you are speaking to a client in a therapy session."
)

def generate_response(user_input):
    try:
        prompt = f"{initial_prompt}\nClient: {user_input}\nTherapist:"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_file = "output.mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)

def record_audio(filename, duration, samplerate=44100):
    print("Recording...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, myrecording, samplerate)
    print("Recording complete")

def speech_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def main():
    print("Hi, I am your therapist! How can I help you today?")
    text_to_speech("Hi, I am your therapist! How can I help you today?")

    quit = False
    while not quit:
        audio_filename = 'output.wav'
        record_duration = 5  # seconds
        record_audio(audio_filename, record_duration)

        user_input = speech_to_text(audio_filename)
        if user_input:
            if user_input.lower() == "quit":
                quit = True
            else:
                response = generate_response(user_input)
                print(response)
                text_to_speech(response)

if __name__ == "__main__":
    main()
