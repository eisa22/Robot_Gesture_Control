from pyedo import edo
import time


class Positions:
    def __init__(self):
        self.home_position = (0, 0, 0, 0, 0, 0)
        self.grid1_position = (21.32, 51.29, 64.62, -5.98, 63.97, 23.75)
        self.grid1_position_hover = (21.32, 45.89, 62.6, -5.67, 71.34, 22.75) #70)
        self.grid2_position = (8.03, 44.45, 77.03, -6.17, 57.04, 10.93)
        self.grid2_position_hover = (8.03, 37.89, 75.1, -5.69, 65.47, 9.93)
        self.grid3_position = (-3.54, 44.42, 77.25, -5.74, 55.69, -0.81)
        self.grid3_position_hover = (-3.54, 37.78, 74.33, -5.26, 64.22, -1.75)
        self.grid4_position = (-15.79, 47.35, 72.27, -4.84, 56.74, -13.66)
        self.grid4_position_hover = (-15.79, 41, 70.32, -4.46, 65.11, -14.44, 47.93)