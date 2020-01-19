import commu

def sync_pos(dev, ip1, ip2):
    data = [{"ip":"","data":""},{"ip":"","data":""}]
    log = [[],[],[]]
    x = input("x = ")
    y = input("y = ")
    log[0] = [x, y]
    if dev == 1:
        #デバイス１番(11号)は２回サーバモード
        data[0] = commu.communication("tcp", "0.0.0.0", 50001).server(x + y)
        log[1] = list(data[0]["data"])
        data[1] = commu.communication("tcp", "0.0.0.0", 50002).server(x + y)
        log[2] = list(data[1]["data"])
    elif dev == 2:
        #デバイス２番(10号)は１回クライアント、１回サーバ
        while data[0]["data"] == "":
            data[0] = commu.communication("tcp", ip1, 50001).client(x + y)
        log[1] = list(data[0]["data"])
        data[1] = commu.communication("tcp", "0.0.0.0", 50003).server(x + y)
        log[2] = list(data[1]["data"])
    elif dev == 3:
        #デバイス３番(12号)は２回クライアント
        while data[0]["data"] == "":
            data[0] = commu.communication("tcp", ip1, 50002).client(x + y)
        log[1] = list(data[0]["data"])
        while data[1]["data"] == "":
            data[1] = commu.communication("tcp", ip2, 50003).client(x + y)
        log[2] = list(data[1]["data"])
    #for i in range(3): print(log[i])
    return log