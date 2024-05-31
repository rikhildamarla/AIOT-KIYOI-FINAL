from flask import Flask, Response
from flask_cors import CORS
import cv2
import mediapipe as mp
import numpy as np
import time
from flask import jsonify
from flask import request
from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
import os
from gtts import gTTS
import time
import google.generativeai as genai



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

@app.route('/cameras')
def get_cameras():
    cameras = ['iPhone Camera', 'FaceTime HD Camera'] 
    return jsonify({'cameras': cameras})

def calculate_angle(a, b, c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def generate_video(camera_index):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        angle_threshold_high = 160
        angle_threshold_low = 90
        success_duration = 3
        success_time = 0
        start_time = 0
        state = "Failure"
        halfway = False

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            all_in_frame = True

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )

                pose_landmarks = results.pose_landmarks.landmark

                left_shoulder = [pose_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 pose_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [pose_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              pose_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [pose_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              pose_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_shoulder = [pose_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  pose_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [pose_landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               pose_landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [pose_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               pose_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                keypoints = [left_shoulder, left_elbow, left_wrist, right_shoulder, right_elbow, right_wrist]
                for point in keypoints:
                    if point[0] < 0 or point[0] > 1 or point[1] < 0 or point[1] > 1:
                        all_in_frame = False
                        break

                if all_in_frame:
                    shoulder_width = np.linalg.norm(np.array(left_shoulder) - np.array(right_shoulder))
                    hand_distance = np.linalg.norm(np.array(left_wrist) - np.array(right_wrist))

                    if hand_distance < shoulder_width:
                        cv2.putText(image, "Move hands to shoulder-width distance", (50, 100), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                    else:
                        angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                        current_time = time.time()

                        if angle > angle_threshold_high:
                            if halfway:
                                print('Up top')
                                if current_time - start_time <= 3:
                                    state = "Success"
                                    success_time = current_time
                                
                                halfway = False
                            else:
                                start_time = current_time
                                print('havent started')
                            
                        elif not halfway and angle < angle_threshold_low:
                            print('halfway')
                            halfway = True
                        
                        if state == "Success" and (current_time - success_time) > success_duration:
                            state = "Failure"

                        cv2.putText(image, str(int(angle)), 
                                    tuple(np.multiply(left_elbow, [image.shape[1], image.shape[0]]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                                   )

                        if state == "Success":
                            cv2.putText(image, "Success", (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        else:
                            cv2.putText(image, "Failure", (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(image, "Ensure elbows, shoulders, forearms, and hands are in the frame", 
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(image, "Ensure elbows, shoulders, forearms, and hands are in the frame", 
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()

@app.route('/video_feed')
def video_feed():
    camera_index = request.args.get('camera', default=0, type=int)
    return Response(generate_video(camera_index), mimetype='multipart/x-mixed-replace; boundary=frame')

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
