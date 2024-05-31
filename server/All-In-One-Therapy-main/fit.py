import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize the Mediapipe Pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point (shoulder)
    b = np.array(b)  # Mid point (elbow)
    c = np.array(c)  # End point (wrist)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize the Pose model
with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    angle_threshold_high = 160
    angle_threshold_low = 90
    success_duration = 3  # duration to show "Success"
    success_time = 0
    start_time = 0
    state = "Failure"
    halfway = False

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and detect the pose
        results = pose.process(image_rgb)

        # Initialize flag for checking all necessary landmarks
        all_in_frame = True

        if results.pose_landmarks:
            # Draw pose landmarks on the original BGR image
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
            )

            # Extract landmarks
            pose_landmarks = results.pose_landmarks.landmark

            # Get coordinates of key points
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
                # Check the distance between hands
                shoulder_width = np.linalg.norm(np.array(left_shoulder) - np.array(right_shoulder))
                hand_distance = np.linalg.norm(np.array(left_wrist) - np.array(right_wrist))

                if hand_distance < shoulder_width:
                    cv2.putText(image, "Move hands to shoulder-width distance", (50, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                else:
                    # Calculate the angle
                    angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                    # Check the angle conditions for success
                    current_time = time.time()
                    if angle > angle_threshold_high:
                        if halfway:
                            print('Up top')
                            if current_time - start_time <= 3:
                                state = "Success"
                                success_time = current_time
                            
                            halfway = False
                        else:
                            #Hasn't started rep
                            start_time = current_time
                            print('havent started')
                        
                    elif not halfway and angle < angle_threshold_low:
                        print('halfway')
                        halfway = True
                    
                    if state == "Success" and (current_time - success_time) > success_duration:
                        state = "Failure"

                    # Display the angle on the image
                    cv2.putText(image, str(int(angle)), 
                                tuple(np.multiply(left_elbow, [image.shape[1], image.shape[0]]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                               )

                    # Display "Success" or "Failure"
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

        # Display the image with pose landmarks and status
        cv2.imshow('MediaPipe Pose Detection', image)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
