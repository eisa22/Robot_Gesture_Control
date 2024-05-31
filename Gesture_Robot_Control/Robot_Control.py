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


    def handle_input(self, choice):
        if choice == '1':
            print("Case 1 - Robot moves to grid 1")
            target_position = Positions.grid1_position
            gripper_open = False
        elif choice == '1o':
            print("Case 1h - Robot moves to grid 1 hover")
            target_position = Positions.grid1_position
            gripper_open = True

        elif choice == '1h':
            print("Case 1h - Robot moves to grid 1 hover")
            target_position = Positions.grid1_position_hover
            gripper_open = False
        elif choice == '1ho':
            print("Case 1h - Robot moves to grid 1 hover")
            target_position = Positions.grid1_position_hover
            gripper_open = True

        elif choice == '2':
            print("Case 2 - Robot moves to grid 2")
            target_position = Positions.grid2_position
            gripper_open = False
        elif choice == '2o':
            print("Case 2 - Robot moves to grid 2")
            target_position = Positions.grid2_position
            gripper_open = True

        elif choice == '2h':
            print("Case 2h - Robot moves to grid 2 hover")
            target_position = Positions.grid2_position_hover
            gripper_open = False
        elif choice == '2ho':
            print("Case 2h - Robot moves to grid 2 hover")
            target_position = Positions.grid2_position_hover
            gripper_open = True

        elif choice == '3':
            print("Case 3 - Robot moves to grid 3")
            target_position = Positions.grid3_position
            gripper_open = False
        elif choice == '3o':
            print("Case 3 - Robot moves to grid 3")
            target_position = Positions.grid3_position
            gripper_open = True

        elif choice == '3h':
            print("Case 3h - Robot moves to grid 3 hover")
            target_position = Positions.grid3_position_hover
            gripper_open = False
        elif choice == '3ho':
            print("Case 3h - Robot moves to grid 3 hover")
            target_position = Positions.grid3_position_hover
            gripper_open = True

        elif choice == '4':
            print("Case 4 - Robot moves to grid 4")
            target_position = Positions.grid4_position
            gripper_open = False
        elif choice == '4o':
            print("Case 4 - Robot moves to grid 4")
            target_position = Positions.grid4_position
            gripper_open = True

        elif choice == '4h':
            print("Case 4h - Robot moves to grid 4 hover")
            target_position = Positions.grid4_position_hover
            gripper_open = False
        elif choice == '4ho':
            print("Case 4h - Robot moves to grid 4 hover")
            target_position = Positions.grid4_position_hover
            gripper_open = True

        elif choice == 'H':
            print("Case H - Robot moves to home")
            target_position = Positions.home_position
            gripper_open = False
        elif choice == 'B':
            print("Case H - Robot moves to home")
            target_position = Positions.arm_bottom
            gripper_open = False
        else:
            print("Invalid input. Please enter 1, 2, 3, 4 or H + h for hovering.")
        return target_position, gripper_open

    def move_Robot(self, target_position, gripper_state):
        print("...............Current Command in Robot Control.........: ", target_position, gripper_state)
        if target_position is None:
            target_position = Positions.home_position
        if gripper_state:
            self.myedo.moveGripper(80)
        else:
            self.myedo.moveGripper(50)
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





