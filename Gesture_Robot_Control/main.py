from Gesture_classifier import HandStateDetector
from Robot_Control import Robot_Control
import threading
import time

def run_handstate_detector(handstate_detector, shared_data, data_lock):
    for target_position, gripper_state in handstate_detector.run():
        print(f"Target Coordinates: {target_position}, Gripper State: {gripper_state}")
        with data_lock:
            shared_data['target_position'] = target_position
            shared_data['gripper_state'] = gripper_state

def run_robot_control(robot_control, shared_data, data_lock):
    while True:
        with data_lock:
            if 'target_position' in shared_data and 'gripper_state' in shared_data:
                target_position = shared_data['target_position']
                gripper_state = shared_data['gripper_state']
                print("______Current Command______: ", target_position, gripper_state)
                robot_control.move_Robot(target_position, gripper_state)
        time.sleep(1.0)

if __name__ == "__main__":
    handstate_detector = HandStateDetector()
    robot_control = Robot_Control("10.42.0.49")  # Initialize with the IP address

    shared_data = {}
    data_lock = threading.Lock()

    # Create threads for the handstate_detector and the robot control
    handstate_detector_thread = threading.Thread(target=run_handstate_detector, args=(handstate_detector, shared_data, data_lock))
    robot_control_thread = threading.Thread(target=run_robot_control, args=(robot_control, shared_data, data_lock))

    # Start the threads
    handstate_detector_thread.start()
    robot_control_thread.start()

    # Wait for both threads to complete (which they won't, as both are infinite loops)
    handstate_detector_thread.join()
    robot_control_thread.join()
