

import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Pose and Hands.
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1,
                    smooth_landmarks=True, enable_segmentation=False,
                    smooth_segmentation=True, min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


def get_angle(p1, p2):
    angle = math.atan2(p2.y - p1.y, p2.x - p1.x) * 180 / math.pi
    return angle


def analyze_arm_direction(shoulder, elbow, wrist):
    # Calculate the angle from shoulder to wrist
    arm_angle = get_angle(shoulder, wrist)

    # Determine the direction based on the arm angle
    if 45 <= arm_angle <= 105:
        return 'BOTTOM'
    elif 0 < arm_angle < 45:
        return 'BOTTOM RIGHT'
    elif -105 < arm_angle < -45:
        return 'TOP'
    elif -45 < arm_angle < 0:
        return 'TOP RIGHT'


def get_hand_state(hand_landmarks, image):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    frame_height, frame_width = image.shape[:2]
    # Convert normalized positions to pixel coordinates
    wrist_y = int(wrist.y * frame_height)
    tip_y = int(tip.y * frame_height)
    # Calculate the distance and adjust the sensitivity based on the distance
    distance = abs(wrist_y - tip_y)
    sensitivity = frame_height * 0.06  # Adjust sensitivity relative to frame height
    return 'OPEN' if distance > sensitivity else 'CLOSED'


cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    pose_results = pose.process(image)
    hand_results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = pose_results.pose_landmarks.landmark
        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        direction = analyze_arm_direction(shoulder, elbow, wrist)
        cv2.putText(image, f'Arm Direction: {direction}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2,
                    cv2.LINE_AA)

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_state = get_hand_state(hand_landmarks, image)
            cv2.putText(image, f'Hand: {hand_state}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
                        cv2.LINE_AA)

    cv2.imshow('Pose and Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()