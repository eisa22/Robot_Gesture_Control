from Gesture_classifier import HandStateDetector
from Robot_Control import Robot_Control
from pyedo import edo
import time
import keyboard
from Positions import Positions

# Global flag to bring robot to home Position when pressing R key
emergancy_stop_off = True  # Start with printing enabled

Positions = Positions()
def on_r_key():
    global emergancy_stop
    emergancy_stop = not emergancy_stop  # Toggle the flag when 'R' is pressed

if __name__ == "__main__":
    handstate_detector = HandStateDetector()
    robot_control = Robot_Control()
    print("Check1")

    robot_control = Robot_Control()
    robot_control.StartUp()
    print("success")
    time.sleep(1.0)


    while True:
        keyboard.add_hotkey('r', on_r_key)
        target_position, gripper_state = handstate_detector.run()
        print("Check2")
        if target_position is None:
            print("No position received")
            break

        if not emergancy_stop_off:
            # Perform Robot Control
            robot_control.move_Robot(Positions.home_position)
            print("DriveHOME")
            time.sleep(3.0)

        else:
            print(" ROBOT MOVES BE CAREFUL!!")
            # Move Robot to home position
            robot_control.move_Robot(target_position, gripper_state)
            time.sleep(3.0)
            print("Check3")
