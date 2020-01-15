from search_route import search_adapter
from sound_local import calcdist
from communication import commu
from search_route import route_main
from stepper_raspi import popen

def motion(start, goal, route):
    routeobj = [[int(y) for y in x] for x in route.split("\n")]
    ada = search_adapter.adapter(start,goal,routeobj)
    nowp = start
    prep = [start[0], start[1]]
    nexp = nowp
    while nexp != goal:
        dif_x = nexp[0] - nowp[0]
        dif_y = nexp[1] - nowp[1]
        if abs(nexp[0] - prep[0]) == 2 or abs(nexp[1] - prep[1]) == 2:
            popen.movefor("s")
        elif (nowp[0] - prep[0] > 0 and nexp[1] - nowp[1] < 0) or (nowp[0] - prep[0] < 0 and nexp[1] - nowp[1] > 0) or (nowp[1] - prep[1] > 0 and nexp[0] - nowp[0] > 0) or (nowp[1] - prep[1] < 0 and nexp[0] - nowp[0] < 0):
            popen.movefor("l")
        elif (nowp[0] - prep[0] > 0 and nexp[1] - nowp[1] > 0) or (nowp[0] - prep[0] < 0 and nexp[1] - nowp[1] < 0) or (nowp[1] - prep[1] > 0 and nexp[0] - nowp[0] < 0) or (nowp[1] - prep[1] < 0 and nexp[0] - nowp[0] > 0):
            popen.movefor("r")
        prep = nowp
        nexp = ada.next()
        nowp = nexp
    print("GOAL")


if __name__=="__main__":
    dev_num = int(input("input device number: "))
    loc = calcdist.Calcdist()
    search =  route_main.route_main_func()
    map = []
    x, y = 0, 0
    serverip = "172.31.150.2"

    while(1):
        data = commu.communication("tcp", serverip, 50007).client(dev_num)
        map = data["data"]
        route = []
        if map == []:
            continue
        else:
            x, y = loc.getcoord()
            data = commu.communication("boradcast", serverip, 50007).client(str(x) + "," + str(y))
            x2 = input("x2=")
            y2 = input("y2=")
            x3 = input("x3=")
            y3 = input("y3=")

            Gpoint, route =search.seachr(dev_num, [x, y], [x2, y2], [x3, y3], map)

            motion([x, y], Gpoint, route)

