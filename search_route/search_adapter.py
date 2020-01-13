class adapter:
    def __init__(self, start, goal, maped=[]):
        self.route = [[],[]]
        self.route_line = []
        self.step = 0
        if not type(start) is list or not type(goal) is list or not type(maped) is list:
            print("start and goal, map must list")
            exit()
        self.route = maped
        self.points = [start, goal]


    def import_map(self, maped):
        self.route = maped
        self.make_route()
        self.step = 0


    def make_route(self):
        if not self.route:
            print("must import map")
            exit()
        vpt = self.points[0]
        while self.points[1] != vpt:
            searchp = [ vpt,
                        [vpt[0]+1, vpt[1]],
                        [vpt[0]-1, vpt[1]],
                        [vpt[0], vpt[1]+1],
                        [vpt[0], vpt[1]-1]
                      ]
            for p in searchp:
                if self.route[p[0]][p[1]] > 0:
                    self.route[p[0]][p[1]] -= 1
                    self.route_line.append(p)
                    vpt = p
                    break


    def now(self):
        if not self.route_line:
            self.make_route()
        return self.route_line[self.step]


    def next(self):
        if not self.route_line:
            self.make_route()
        self.step += 1
        if self.step == len(self.route_line):
            self.step = len(self.route_line)
        return self.route_line[self.step-1]
