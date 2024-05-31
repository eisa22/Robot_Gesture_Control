from Gesture_classifier import HandStateDetector
from Robot_Control import Robot_Control
import threading
from queue import Queue
import time

def run_handstate_detector(handstate_detector, move_queue):
    for target_position, gripper_state in handstate_detector.run():
        print(f"Target Coordinates: {target_position}, Gripper State: {gripper_state}")
        move_queue.put((target_position, gripper_state))

def run_robot_control(robot_control, move_queue):
    while True:
        if not move_queue.empty():
            target_position, gripper_state = move_queue.get()
            robot_control.moveRobot(target_position, gripper_state)
            time.sleep(3.0)

if __name__ == "__main__":
    handstate_detector = HandStateDetector()
    robot_control = Robot_Control("10.42.0.49")  # Initialize with the IP address

    move_queue = Queue()

    # Create threads for the handstate_detector and the robot control
    handstate_detector_thread = threading.Thread(target=run_handstate_detector, args=(handstate_detector, move_queue))
    robot_control_thread = threading.Thread(target=run_robot_control, args=(robot_control, move_queue))

    # Start the threads
    handstate_detector_thread.start()
    robot_control_thread.start()

    # Wait for both threads to complete (which they won't, as both are infinite loops)
    handstate_detector_thread.join()
    robot_control_thread.join()