from pyedo import edo
import time
from Positions import Positions

Positions = Positions()

class Robot_Control:

    def __int__(self, myedo):
        self.myedo = myedo


    def StartUp(self):
        self.myedo = edo("10.42.0.49")  # ('10.42.0.49') #192.168.12.1
        self.myedo.init7Axes()
        print("Init startup")
        time.sleep(5)
        self.myedo.disengageStd()
        time.sleep(5)
        self.myedo.calibAxes() # Mandatory in HOME POSITION
        self.myedo.disengageSafe()
        self.myedo.disengageSin()

    def handle_input(self, choice):
        if choice == '1':
            print("Case 1 - Robot moves to grid 1")
            target_position = Positions.grid1_position
        elif choice == '1h':
            print("Case 1h - Robot moves to grid 1 hover")
            target_position = Positions.grid1_position_hover
        elif choice == '2':
            print("Case 2 - Robot moves to grid 2")
            target_position = Positions.grid2_position
        elif choice == '2h':
            print("Case 2h - Robot moves to grid 2 hover")
            target_position = Positions.grid2_position_hover
        elif choice == '3':
            print("Case 3 - Robot moves to grid 3")
            target_position = Positions.grid3_position
        elif choice == '3h':
            print("Case 3h - Robot moves to grid 3 hover")
            target_position = Positions.grid3_position_hover
        elif choice == '4':
            print("Case 4 - Robot moves to grid 4")
            target_position = Positions.grid4_position
        elif choice == '4h':
            print("Case 4h - Robot moves to grid 4 hover")
            target_position = Positions.grid4_position_hover
        elif choice == 'H':
            print("Case H - Robot moves to home")
            target_position = Positions.home_position
        else:
            print("Invalid input. Please enter 1, 2, 3, 4 or H + h for hovering.")
        return target_position

    def move_Robot(self, target_position, gripper_state):
        self.myedo.moveJoints(*target_position)
        if gripper_state:
            self.myedo.moveGripper(50)
        else:
            self.myedo.moveGripper(0)
        time.sleep(3)
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

    robot_control = Robot_Control()

    myedo = edo("10.42.0.49") # ('10.42.0.49') #192.168.12.1
    myedo.disconnect()
    myedo.connect()
    myedo.unblock()
    myedo.verboseOn()
    robot_control.StartUp(myedo)
    myedo.unblock()
    print("success")
    time.sleep(1.0)


    while True:
        # Eingabe einlesen
        user_input = input("Type in 1, 2, 3, 4 oder H or R for reset --> add h for hover position: ")

        if user_input == "R" :
            myedo.disconnect()

        # Eingabe verarbeiten
        target_position = robot_control.handle_input(user_input)

        if target_position is None:
            print("No position received")
            break
        # Perform Robot Control
        gripper_State = False
        robot_control.move_Robot(target_position, gripper_State)
        print("targetPos: ", target_position, "current Pos: ", myedo.getJoints)
        #wait_until_position_reached(myedo.getJoints, target_position)
        time.sleep(3.0)

        # Wait until robot reaches Position


#myedo.disconnect()
