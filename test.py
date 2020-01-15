import system
from stepper_raspi import popen

data = open("route.txt", "r").readlines()
map_ = ""
for x in data : map_ += x
start = [1,1]
goal = [5,5]
print(start)
print(goal)
print(map_)
system.motion(start,goal,map_)
