from sond_localization import calcdist
from communication import commu
from search_route import route_main

if __name__=="__main__":"
    dev_num = int(input("input device numver: "))
    loc = Calcdist()
    search =  Route_main()
    map = []
    x, y = 0, 0
    serverip = ""
    
    def motion(x, y, route):
        while True:
            next_x, next_y = next(x, y, route)
            dif_x = next_x - x
            dif_y = next_y - y
            if dif_x < 0 and dif_y == 0:
                move("R")
            elif dif_x > 0 and dif_Y == 0:
                move("L")
            elif dif_y > 0 and dif_x == 0:
                move("S")
            elif dif_x == 0 and dif_Y == 0:
                print("GOAL")
                break


    while(1):
        data = commu.communication("tcp", serverip, 50007).client("1")
        map = data["data"]
        route = []
        if map == []:
            continue
        else:
            x, y = loc.getcoord()
            data = commu.communication("tcp", serverip, 50007).client(str(x) + "," + str(y))
            route =search.seachr(x1, y1, x2, y2, x3, y3, map, dev_num)
            
            motion(x, y, route)

