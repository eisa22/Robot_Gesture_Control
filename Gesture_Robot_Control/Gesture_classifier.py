import cv2
import mediapipe as mp
import math
import time
from Positions import Positions

Positions = Positions()
class HandStateDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=1,
                                       smooth_landmarks=True, enable_segmentation=False,
                                       smooth_segmentation=True, min_detection_confidence=0.5,
                                       min_tracking_confidence=0.5)
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                                         min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.system_on_off = False  # Initial state of the system
        self.gripper_state = False  # Initial state of the gripper
        self.pose_start_time = False  # Time when the pose is first detected
        self.last_state = 'OPEN'
        self.last_closed_time = None
        self.close_count = 0
        self.last_direction = None
        self.last_direction_change_time = 0

    def get_hand_state(self, hand_landmarks, image):
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        fingertips = [hand_landmarks.landmark[i] for i in [self.mp_hands.HandLandmark.THUMB_TIP,
                                                           self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                                           self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                                                           self.mp_hands.HandLandmark.RING_FINGER_TIP,
                                                           self.mp_hands.HandLandmark.PINKY_TIP]]

        frame_height, frame_width = image.shape[:2]
        wrist_pos = (wrist.x * frame_width, wrist.y * frame_height)
        open_fingers = sum(math.sqrt(
            (tip.x * frame_width - wrist_pos[0]) ** 2 + (tip.y * frame_height - wrist_pos[1]) ** 2) > frame_height * 0.1
                           for tip in fingertips)

        current_time = time.time()
        if open_fingers >= 3:
            self.last_state = 'OPEN'
        else:
            if self.last_state == 'OPEN':
                if self.last_closed_time is None or (current_time - self.last_closed_time < 2):
                    self.close_count += 1
                else:
                    self.close_count = 1
                self.last_closed_time = current_time
            self.last_state = 'CLOSED'

        return self.last_state, self.close_count

    def check_horizontal_pose(self, shoulder, wrist):
        """ Check if the wrist is horizontally aligned with the shoulder. """
        tolerance = 0.1  # Allowable vertical distance ratio to consider aligned
        return abs(wrist.y - shoulder.y) < tolerance

    def toggle_system(self, pose_landmarks):
        """ Toggle the system on/off based on the pose of the arms. """
        current_time = time.time()
        if pose_landmarks:
            left_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]

            left_aligned = self.check_horizontal_pose(left_shoulder, left_wrist)
            right_aligned = self.check_horizontal_pose(right_shoulder, right_wrist)

            if left_aligned and right_aligned:
                if self.pose_start_time is None:
                    self.pose_start_time = current_time
                elif current_time - self.pose_start_time >= 2:
                    self.system_on_off = not self.system_on_off
                    self.pose_start_time = None  # Reset timer after toggling
            else:
                self.pose_start_time = None  # Reset timer if pose is not maintained

    def analyze_arm_direction(self, shoulder, elbow, wrist):
        """ Determine the arm direction based on the angle of the arm. """
        angle = math.atan2(wrist.y - shoulder.y, wrist.x - shoulder.x) * 180 / math.pi
        if 45 <= angle <= 135:
            direction = 'BOTTOM'
        elif 0 <= angle < 45:
            direction = 'BOTTOM RIGHT'
        elif -135 < angle < -45:
            direction = 'TOP'
        elif -45 < angle < 0:
            direction = 'TOP RIGHT'
        else:
            direction = None

        if direction != self.last_direction:
            if time.time() - self.last_direction_change_time < 3:
                return self.last_direction
            else:
                self.last_direction_change_time = time.time()
                self.last_direction = direction

        return direction

    def process_gripper_state(self, close_count):
        current_time = time.time()
        if close_count == 1:
            self.first_closed_time = current_time
        if close_count == 2:
            if current_time - self.first_closed_time <= 3:
                self.gripper_state = False if self.gripper_state else True
                self.close_count = 0  # Reset close count after processing state change
                return True
            else:
                self.close_count = 0  # Reset close count if 3 closes did not occur within 3 seconds
        return False

    def hand_to_position(self, hand_state, gripper_state):
        target_position = None  # Initialize target_position to None
        print("Handstate: ", hand_state)
        print("Gripper State: ", gripper_state)
        if (hand_state == 'BOTTOM' and gripper_state):
            print("Case BOTTOM down - Robot moves to grid 1")
            target_position = Positions.grid1_position
        elif hand_state == 'BOTTOM':
            print("Case BOTTOM HOVER - Robot moves to grid 1 hover")
            target_position = Positions.grid1_position_hover
        elif (hand_state == 'BOTTOM RIGHT' and gripper_state):
            print("Case BOTTOM RIGHT - Robot moves to grid 2")
            target_position = Positions.grid2_position
        elif hand_state == 'BOTTOM RIGHT':
            print("Case BOTTOM RIGHT HOVER - Robot moves to grid 2 hover")
            target_position = Positions.grid2_position_hover
        elif (hand_state == 'TOP' and gripper_state):
            print("Case TOP - Robot moves to grid 3")
            target_position = Positions.grid3_position
        elif hand_state == 'TOP':
            print("Case TOP HOVER - Robot moves to grid 3 hover")
            target_position = Positions.grid3_position_hover
        elif (hand_state == 'TOP RIGHT' and gripper_state):
            print("Case TOP RIGHT - Robot moves to grid 4")
            target_position = Positions.grid4_position
        elif hand_state == 'TOP RIGHT':
            print("Case TOP RIGHT HOVER - Robot moves to grid 4 hover")
            target_position = Positions.grid4_position_hover
        else:
            print("No position detected - Adjust position!")
        return target_position

    def run(self):
        cap = cv2.VideoCapture(0)
        target_coordinates = Positions.home_position



        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")


        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        pose_results = self.pose.process(image)
        hand_results = self.hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if pose_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            self.toggle_system(pose_results.pose_landmarks)
            landmarks = pose_results.pose_landmarks.landmark
            shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
            arm_direction = self.analyze_arm_direction(shoulder, elbow, wrist)

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                hand_state, close_count = self.get_hand_state(hand_landmarks, image)
                target_coordinates = self.hand_to_position(arm_direction, self.gripper_state)
                if self.process_gripper_state(close_count):
                    print(f'Gripper state changed to {self.gripper_state}')



        cv2.putText(image, f'Arm Direction: {arm_direction}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2,
                    cv2.LINE_AA)
        cv2.putText(image, f'Gripper State: {self.gripper_state}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2,
                    cv2.LINE_AA)
        cv2.putText(image, f'System ON/OFF: {"ON" if self.system_on_off else "OFF"}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Pose and Hand Tracking', image)

        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()


        return target_coordinates, self.gripper_state

# = HandStateDetector()
#hand_state_detector.run()
