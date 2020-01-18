import commu
data = dict()
log = [[],[],[]]
val = ""
status = 0
dev = int(input("device num: "))
x = input("x = ")
y = input("y = ")
log[0] = [x, y]
if dev == 1:
    #デバイス１番(11号)は２回サーバモード
    for i in range(2):
        data[i] = commu.communication("tcp", "0.0.0.0", 50000+i).server(x + y)
        log[i+1] = list(data[i]["data"])
elif dev == 2:
    #デバイス２番(10号)は１回クライアント、１回サーバ
    while data[0]["data"] != "":
        data[0] = commu.communication("tcp", "172.31.150.11", 50001.client(x + y)
    log[1] = list(data[0]["data"])
    data[1] = commu.communication("tcp", "0.0.0.0", 50003).server(x + y)
    log[2] = list(data[1]["data"])

elif dev == 3:
    #デバイス３番(12号)は２回クライアント
    while data[0]["data"] != "":
        data[0] = commu.communication("tcp", "172.31.150.11", 50002).client(x + y)
    log[1] = list(data[0]["data"])
    while data[1]["data"] != "":
        data[1] = commu.communication("tcp", "127.0.0.10", 50003).client(x + y)
    log[2] = list(data[1]["data"])
print(log[0])
print(log[1])
print(log[2])
while status != 1:
    val = commu.communication("tcp", "172.31.150.2", 50007).client("1: ready")
    status = int(val)
print("end")