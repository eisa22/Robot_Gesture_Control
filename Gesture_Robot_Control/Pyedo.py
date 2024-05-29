from pyedo import edo
import time

def StartUp(myedo):
    myedo.init_7Axes()
    print("Init startup")
    time.sleep(5)
    myedo.disengage_std()
    time.sleep(5)
    myedo.calib_axes() # Mandatory in HOME POSITION

# Positions
# Positions
home_position = (100, 0, 0, 0, 0, 0, 0, 20)
grid1_position = (100, 21.32, 51.29, 64.62, -5.98, 63.97, 23.75, 70)
grid1_position_hover = (100, 21.32, 45.89, 62.6, -5.67, 71.34, 22.75, 70)
grid2_position = (100, 8.03, 44.45, 77.03, -6.17, 57.04, 10.93, 70)
grid2_position_hover = (100, 8.03, 37.89, 75.1, -5.69, 65.47, 9.93, 70)
grid3_position = (100, -3.54, 44.42, 77.25, -5.74, 55.69, -0.81, 70)
grid3_position_hover = (100, -3.54, 37.78, 74.33, -5.26, 64.22, -1.75, 70)
grid4_position = (100, -15.79, 47.35, 72.27, -4.84, 56.74, -13.66, 70 )
grid4_position_hover = (100, -15.79, 41, 70.32, -4.46, 65.11, -14.44, 47.93, 70)

if __name__ == "__main__":

    myedo = edo("10.42.0.49") #('10.42.0.49') #192.168.12.1
    StartUp(myedo)
    print("success")


    time.sleep(1)

    time.sleep(1)

    myedo.move_joint(*home_position)

    time.sleep(1)

    myedo.move_joint(100, 20, 0, 0, 0, 0, 0, 0)