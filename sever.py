from communication import commu

while True:
    filenum = input("select map: ")
    data = open(filenum,"r").readlines()
    map_ = ""
    for x in data: map_ += x
    #print(commu.communication("tcp", "172.31.150.10", 50007).server(map_))
    print(commu.communication("tcp", "172.31.150.11", 50007).server(map_))
    #print(commu.communication("tcp", "172.31.150.12", 50007).server(map_))