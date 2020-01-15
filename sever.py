from communication import commu

filenum = input("select map: ")
f = open(filenum, "r")
data = f.read(512)
print(commu.communication("tcp", "172.31.150.11", 50007).server(data)