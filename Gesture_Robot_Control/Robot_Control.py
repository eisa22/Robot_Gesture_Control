from pyedo import edo
import time
from Positions import Positions

Positions = Positions()

class Robot_Control:
    def __init__(self, ip_address="10.42.0.49"):
        self.positions = Positions
        self.myedo = edo(ip_address)
        self.myedo.disconnect()
        self.myedo.connect()
        self.myedo.unblock()
        self.myedo.verboseOn()
        self.StartUp()
        self.myedo.unblock()
        print("success")
        time.sleep(1.0)

    def StartUp(self):
        #myedo = edo("10.42.0.49")  # ('10.42.0.49') #192.168.12.1
        self.myedo.disconnect()
        self.myedo.connect()
        self.myedo.unblock()
        self.myedo.verboseOn()

        self.myedo.init7Axes()
        print("Init startup")
        time.sleep(5)
        self.myedo.disengageStd()
        time.sleep(5)
        self.myedo.calibAxes()  # Mandatory in HOME POSITION
        self.myedo.disengageSafe()
        self.myedo.disengageSin()

        self.myedo.unblock()
        print("success")
        time.sleep(1.0)



    def move_Robot(self, target_position, gripper_state):
        print("...............Current Command in Robot Control.........: ", target_position, gripper_state)
        if target_position is None:
            pass
        else:
            if gripper_state:
                self.myedo.moveGripper(80)
                print("Gripper open ...............................")
            else:
                self.myedo.moveGripper(50)
                print("Gripper closed ...............................")
            self.myedo.moveJoints(*target_position)
        time.sleep(1)
        return True


    def wait_until_position_reached(self, current_position, target_position):
        while True:
            # If the current position is the same as the target position, break the loop
            if current_position == target_position:
                print("Target Position reached!")
                break
            # Otherwise, wait for a short period before checking again
            time.sleep(0.1)
        return True




if __name__ == "__main__":

    myedo = edo("10.42.0.49") # ('10.42.0.49') #192.168.12.1
    myedo.disconnect()
    myedo.connect()
    myedo.unblock()
    myedo.verboseOn()
    StartUp(myedo)
    myedo.unblock()
    print("success")
    time.sleep(1.0)


    while True:
        # Eingabe einlesen
        #user_input = input("Type in 1, 2, 3, 4 oder H or R for reset or B --> add h for hover position or o for open gripper: ")



        # Eingabe verarbeiten
        #target_position, gripper_open = handle_input(user_input)
        time.sleep(5.0)
        target_position, gripper_open = handle_input("1ho")
        move_Robot(target_position, gripper_open)
        time.sleep(3.0)
        target_position, gripper_open = handle_input("1o")
        move_Robot(target_position, gripper_open)
        time.sleep(2.5)
        target_position, gripper_open = handle_input("1")
        move_Robot(target_position, gripper_open)
        time.sleep(2.0)
        target_position, gripper_open = handle_input("1h")
        move_Robot(target_position, gripper_open)
        time.sleep(3.0)
        target_position, gripper_open = handle_input("4h")
        move_Robot(target_position, gripper_open)
        time.sleep(2.5)
        target_position, gripper_open = handle_input("4")
        move_Robot(target_position, gripper_open)
        time.sleep(2.5)
        target_position, gripper_open = handle_input("4o")
        move_Robot(target_position, gripper_open)
        time.sleep(1.5)
        target_position, gripper_open = handle_input("4ho")
        move_Robot(target_position, gripper_open)
        time.sleep(4.0)

        target_position, gripper_open = handle_input("3ho")
        move_Robot(target_position, gripper_open)
        time.sleep(2.5)
        target_position, gripper_open = handle_input("3o")
        move_Robot(target_position, gripper_open)
        time.sleep(2.0)
        target_position, gripper_open = handle_input("3")
        move_Robot(target_position, gripper_open)
        time.sleep(1.5)
        target_position, gripper_open = handle_input("3h")
        move_Robot(target_position, gripper_open)
        time.sleep(3.0)
        target_position, gripper_open = handle_input("2h")
        move_Robot(target_position, gripper_open)
        time.sleep(1.0)
        target_position, gripper_open = handle_input("2")
        move_Robot(target_position, gripper_open)
        time.sleep(2.5)
        target_position, gripper_open = handle_input("2o")
        move_Robot(target_position, gripper_open)
        time.sleep(1.0)
        target_position, gripper_open = handle_input("2ho")
        move_Robot(target_position, gripper_open)

        time.sleep(3.0)
        target_position, gripper_open = handle_input("H")
        move_Robot(target_position, gripper_open)

        time.sleep(5.0)





