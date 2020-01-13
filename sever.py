from communication import commu

filenum = input("select map: ")
f = open(filenum, "r")
data = f.read(512)
print(commu.communication("tcp", "127.0.0.1", 50007).server(data)
