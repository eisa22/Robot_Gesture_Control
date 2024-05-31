from Gesture_classifier import HandStateDetector
from Robot_Control import Robot_Control
import threading
import time

class SharedData:
    def __init__(self):
        self.data = []
        self.lock = threading.Lock()

    def update(self, target_position, gripper_state):
        with self.lock:
            if len(self.data) >= 2:
                self.data.pop(0)  # Remove the oldest item
            self.data.append((target_position, gripper_state))

    def get_latest(self):
        with self.lock:
            if self.data:
                return self.data[-1]
            return None

def run_handstate_detector(handstate_detector, shared_data):
    for target_position, gripper_state in handstate_detector.run():
        print(f"Target Coordinates: {target_position}, Gripper State: {gripper_state}")
        shared_data.update(target_position, gripper_state)

def run_robot_control(robot_control, shared_data):
    while True:
        latest_command = shared_data.get_latest()
        if latest_command:
            target_position, gripper_state = latest_command
            print("______Current Command______: ", target_position, gripper_state)
            robot_control.move_Robot(target_position, gripper_state)
        else:
            print("!!!!!!!!!!!!!!!!!!NO COMMAND AVAILABLE!!!!!!!!!!!!!!!!!!")
        time.sleep(1.0)

if __name__ == "__main__":
    handstate_detector = HandStateDetector()
    robot_control = Robot_Control("10.42.0.49")  # Initialize with the IP address

    shared_data = SharedData()

    # Create threads for the handstate_detector and the robot control
    handstate_detector_thread = threading.Thread(target=run_handstate_detector, args=(handstate_detector, shared_data))
    robot_control_thread = threading.Thread(target=run_robot_control, args=(robot_control, shared_data))

    # Start the threads
    handstate_detector_thread.start()
    robot_control_thread.start()

    # Wait for both threads to complete (which they won't, as both are infinite loops)
    handstate_detector_thread.join()
    robot_control_thread.join()
