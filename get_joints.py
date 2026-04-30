import urx
import math3d as m3d
from time import sleep
from config import load_config

robot = urx.Robot(load_config().surgeon_ip)

pos = robot.get_pos()
print(pos)
robot.close()
