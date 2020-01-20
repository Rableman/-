from communication import commu

while True:
	inp = input()
	if inp == "position":
		filename = "test.dat"
		print("", end="", file=open(filename, "w"))
		while True:
			s = input()
			if s == "":
				break
			print(s, file=open(filename, "a"))
		print(open(filename, "r").read())
		break
	else:
		print(inp)

while True:
    data = open(filename,"r").readlines()
    map_ = ""
    for x in data: map_ += x
    #print(commu.communication("tcp", "172.31.150.10", 50007).server(map_))
    print(commu.communication("tcp", "172.31.150.11", 50007).server(map_))
    #print(commu.communication("tcp", "172.31.150.12", 50007).server(map_))
