import sys
from search_route import search_adapter
from sound_local import calcdist
from communication import commu
from search_route import route_main
from stepper_raspi import popen
import subprocess

if __name__=="__main__":
    result = subprocess.check_output('ip a | grep -o "172.31.[0-9]*.[0-9]*/24"', shell=True)
    result = [x for x in result.split("\n") if x][0]
    result = result[:len(result)-3]
    if result == "172.31.150.10":
        dev_num = 2
        Gpoint = [2, 1]
    elif result == "172.31.150.11":
        dev_num = 1
        Gpoint = [1, 1]
    elif result == "172.31.150.12":
        dev_num = 3
        Gpoint = [3, 1]
    #loc = calcdist.Calcdist()
    search =  route_main.route_main_func()
    map = []
    pos = [[],[],[]]
    serverip = "172.31.100.1"
    args = sys.argv
    ip1 = "172.31.150.11"
    ip2 = "172.31.150.10"
    ip3 = "172.31.150.12"

    while(1):
        data = commu.communication("tcp", serverip, 50007).client(str(dev_num))
        map = data["data"]
        print(map)
        route = []
        if map == []:
            continue
        else:
            #x, y = loc.get_coord()
            pos = sync_pos(dev_num, [ip1, ip2, ip3], Gpoint)
            Gpoint, route = search.main(dev_num, (pos[0][0], pos[0][1]), (pos[1][0], pos[1][1]), (pos[2][0], pos[2][1]), map)
            #print(Gpoint, route)
            motion([x, y], Gpoint, route)

def motion(start, goal, route):
    routeobj = [[int(y) for y in x] for x in route.split("\n")]
    ada = search_adapter.adapter(start,goal,routeobj)
    nowp = [0, 0]
    prep = [0, 0]
    nexp = start
    while nexp != goal:
        nexp = ada.next()
        dif_x = nexp[0] - nowp[0]
        dif_y = nexp[1] - nowp[1]
        if abs(nexp[0] - prep[0]) == 2 or abs(nexp[1] - prep[1]) == 2:
            popen.movefor("s")
        elif (nowp[0] - prep[0] > 0 and nexp[1] - nowp[1] < 0) or (nowp[0] - prep[0] < 0 and nexp[1] - nowp[1] > 0) or (nowp[1] - prep[1] > 0 and nexp[0] - nowp[0] > 0) or (nowp[1] - prep[1] < 0 and nexp[0] - nowp[0] < 0):
            popen.movefor("l")
        elif (nowp[0] - prep[0] > 0 and nexp[1] - nowp[1] > 0) or (nowp[0] - prep[0] < 0 and nexp[1] - nowp[1] < 0) or (nowp[1] - prep[1] > 0 and nexp[0] - nowp[0] < 0) or (nowp[1] - prep[1] < 0 and nexp[0] - nowp[0] > 0):
            popen.movefor("r")
        prep = nowp
        nowp = nexp
    print("GOAL")


def sync_pos(dev, ipadder, nowp):
    data = [{"ip":"","data":""},{"ip":"","data":""}]
    log = [[],[],[]]
    log[0] = nowp
    if dev == 1:
        #デバイス１番(11号)は２回サーバモード
        data[0] = commu.communication("tcp", "0.0.0.0", 50001).server(x + y)
        log[1] = list(data[0]["data"])
        data[1] = commu.communication("tcp", "0.0.0.0", 50002).server(x + y)
        log[2] = list(data[1]["data"])
    elif dev == 2:
        #デバイス２番(10号)は１回クライアント、１回サーバ
        while data[0]["data"] == "":
            data[0] = commu.communication("tcp", ipadder[0], 50001).client(x + y)
        log[1] = list(data[0]["data"])
        data[1] = commu.communication("tcp", "0.0.0.0", 50003).server(x + y)
        log[2] = list(data[1]["data"])
    elif dev == 3:
        #デバイス３番(12号)は２回クライアント
        while data[0]["data"] == "":
            data[0] = commu.communication("tcp", ipadder[0], 50002).client(x + y)
        log[1] = list(data[0]["data"])
        while data[1]["data"] == "":
            data[1] = commu.communication("tcp", ipadder[1], 50003).client(x + y)
        log[2] = list(data[1]["data"])
    #for i in range(3): print(log[i])
    for i in range(3):
        for j in range(2):
            log[i][j] = int(log[i][j])
    return log
